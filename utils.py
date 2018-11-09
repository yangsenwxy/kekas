from functools import reduce

from tqdm import tqdm


def to_numpy(data):
    return data.detach().cpu().numpy()


def exp_weight_average(curr_val, prev_val, alpha=0.9, from_torch=True):
    if from_torch:
        curr_val = to_numpy(curr_val)
    return alpha * prev_val + (1 - alpha) * curr_val


def get_trainval_pbar(epoch, epochs, dataloader):

    pbar = tqdm(
        total=len(dataloader),
        leave=True,
        ncols=0,
        desc=f"Epoch {epoch+1}/{epochs}")

    return pbar


def get_predict_pbar(dataloader):
    pbar = tqdm(
        total=len(dataloader),
        leave=True,
        ncols=0,
        desc="Predict")

    return pbar


def extend_postfix(postfix, dct):
    postfixes = [postfix] + [f"{k}={v:.4f}" for k, v in dct.items()]
    return ", ".join(postfixes)

# TODO: REMOVE
def update_epoch_metrics(target, preds, metrics, epoch_metrics):
    for m in metrics:
        value = m(target, preds)
        epoch_metrics[m.__name__] += value


def get_opt_lr(opt):
    # TODO: rewrite it for differentrial learning rates
    lrs = [pg["lr"] for pg in opt.param_groups]
    res = reduce(sum, lrs) / len(lrs)
    return res


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__