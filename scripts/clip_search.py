"""Optional Chinese-CLIP inference. Requires user's images and model download."""
import argparse, json
from pathlib import Path

def main():
    import torch
    import cn_clip.clip as clip
    from cn_clip.clip import load_from_name
    from PIL import Image
    from retrieval import BM25, rrf
    p=argparse.ArgumentParser()
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--query', required=True)
    p.add_argument('--device', default='cpu')
    p.add_argument('--model', default='ViT-B-16')
    p.add_argument('--k', type=int, default=10)
    p.add_argument('--hybrid', action='store_true')
    args=p.parse_args()
    if args.k <= 0: p.error('--k must be positive')
    docs=json.loads(args.manifest.read_text())
    if not docs or len({d['id'] for d in docs}) != len(docs):
        raise ValueError('manifest must contain unique IDs and at least one image')
    model, preprocess=load_from_name(args.model, device=args.device, download_root='./models')
    model.eval()
    features=[]
    with torch.no_grad():
        for doc in docs:
            path=(args.manifest.parent/doc['image']).resolve()
            with Image.open(path) as im:
                # First-frame baseline for GIF; multi-frame aggregation is an extension.
                batch=preprocess(im.convert('RGB')).unsqueeze(0).to(args.device)
            feature=model.encode_image(batch).float()
            features.append(torch.nn.functional.normalize(feature,dim=-1))
        bank=torch.cat(features)
        q=model.encode_text(clip.tokenize([args.query]).to(args.device)).float()
        q=torch.nn.functional.normalize(q,dim=-1)
        scores=(q @ bank.T)[0].cpu().tolist()
    by_id={doc['id']:doc for doc in docs}
    dense=[docs[i]['id'] for i in sorted(range(len(docs)),key=lambda i:(-scores[i],docs[i]['id']))]
    result=dense
    if args.hybrid:
        lexical=[x for x,s in BM25(docs).search(args.query,min(100,len(docs)))]
        result=rrf([dense[:100],lexical])
    print(json.dumps([{'id':i,'text':by_id[i]['text'],'image':by_id[i]['image']} for i in result[:args.k]],ensure_ascii=False,indent=2))
if __name__=='__main__': main()
