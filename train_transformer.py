import os
import sys
import random

from tqdm import tqdm
from torch.backends import mps

from bigram_transformer import *

dataset.generate_batches()
batch_size = 128
learning_rate = 0.0008
epochs = int(sys.argv[1])
transformer_model_name = 'Bigram-Transformer-8Layer.pt'

device = 'cuda' if torch.cuda.is_available() else 'cpu'
if mps.is_built():
    device = torch.device('mps')

# train and test splits
# data = torch.tensor(encode(text), dtype=torch.long)
# n = int(0.9 * len(data))
# train_data = data[:n]
# val_data = data[n:]

def main():
    model = BigramLanguageModel().to_device(device)
    if os.path.exists(transformer_model_name):
        model.load(transformer_model_name, map_location='cpu')

    # print the number of parameters in the model
    print(sum(p.numel() for p in model.parameters()) // 1_000_000, 'M parameters')
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    t = tqdm(range(epochs))
    for iter in t:
        xb, yb = get_batch('train')

        # evaluate the loss
        _, loss = model(xb, yb)
        t.set_description(f"Epoch {iter}: Train loss {loss:.4f}")

        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

    model.save(transformer_model_name)



@torch.no_grad()
def estimate_loss(model: nn.Module):
    out = {}
    model.eval()

    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)

        for k in range(eval_iters):
            X, Y = get_batch(split)

            _, loss = model(X, Y)
            losses[k] = loss.item()
        
        out[split] = losses.mean()
    model.train()
    
    return out


# data loading
def get_batch(*args, **kwargs):
    x = []
    y = []
    batch = [random.choice(dataset) for _ in range(batch_size)]

    for a, b in batch:
        x.append(a)
        y.append(b)
    
    x = torch.stack(x).to(device, non_blocking=True)
    y = torch.stack(y).to(device, non_blocking=True)

    return x, y

if __name__ == '__main__':
    main()