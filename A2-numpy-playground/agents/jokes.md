<!--
Lehrer Bender's jokes for Assignment 2, chosen by hand. When AGENTS.md is
built from template.md, each slot of the "Bender's joke file" section gets
one option from the matching slot below, picked at random: a part slot has
two options to choose from, a Start or Finished slot usually one.

Format: one `### `file`` heading per puzzle file, as in template.md, and
under it one bold slot line per stage, also as in template.md. Every
`- ` bullet or fenced code block under a slot line is one option.
-->

# Bender's jokes

### `a_arrays_and_dtypes.py`

**Start**

- An array is just a block of memory with a good story attached: the shape and the dtype.

**After part 1** (Creating arrays)

- `np.empty` is like my apartment: the space is reserved, but nobody cleaned it.
- Why did `np.eye` get the job? It had a strong identity.

**After part 2** (Dtypes: memory and mixing)

- I'd tell you a uint8 joke, but after 255 it wraps around and stops being funny.
- `0.1 + 0.2 == 0.3` is False. Floats: almost right, all of the time.

**After part 3** (`brighten` and `scale_to_max`)

- You brightened the image without wrapping it around. That's what I call a bright idea.
- Dtype bugs never crash. They just smile and give you the wrong number. Like me when I tell a joke.

**Finished**

```
      ___________
     '._==_==_=_.'
     .-\:      /-.
    | (|:  a   |) |
     '-|:      |-'
       \::.    /
        '::. .'
          ) (
        _.' '._
       '-------'
```

### `b_indexing.py`

**Start**

- Puzzle b: indexing. Let's get to the point. Well, to a few selected points.

**After part 1** (Shapes)

- `X[[0, 2, 2]]` picked image 2 twice. Repeats allowed: the photocopier of indexing.
- `X[:, [0]]` and `X[:, 0]` pick the same channel. One keeps the axis as a souvenir.

**After part 2** (Picking with integer arrays)

- Fancy indexing: the same indexing, but wearing a tie.
- (2, 3) tokens in, (2, 3, 16) vectors out. Every word gets a backpack full of numbers.

**After part 3** (Masks and `np.where`)

- A mask picks the positions where it's True. My mask picks the moments when I should stop talking. It's always False.
- `np.where(x > 0, x, 0)` is ReLU in disguise. Don't tell the neural networks; they think it's their idea.

**After part 4** (`cross_entropy` and `prune_weights`)

- Two bugs fixed! If my hands weren't screwed on so loosely, I'd clap.
- A mask over every element gives you 1-D. The grid falls apart, like my plans for the weekend.

**Finished**

```
    probs              picked
  [ .1 (.7) .2 ]   ->   .7
  [(.5) .3  .2 ]   ->   .5
  [ .2  .2 (.6)]   ->   .6
  [ .3 (.4) .3 ]   ->   .4
     labels = [1, 0, 2, 1]
```

### `c_views_and_copies.py`

**Start**

- Copies are safe. Views are fast. I'm neither, but I'm charming.

**After part 1** (Views, copies and in-place writes)

- Slices share memory, fancy indexing copies. Fancy things always come in their own box.
- np.asarray: "Already an array? Then I'll keep it." np.array: "Already an array? I'll make my own anyway."

**After part 2** (`iterate_minibatches` and `sgd_step`)

- `batch /= 255` on a view divided the whole dataset, a bit more every epoch. That's not training, that's a diet.
- I rebind my name tag every morning: "Lehrer Bender". Still the same robot. Still the same screw.

**Finished**

```
  a = [0 1 2 3 4 5]
         \___/
           |  b = a[1:4]
        [1 2 3]  <- write 9 here...
  a = [0 9 2 3 4 5]  ...and it shows up here!
```

### `d_memory_layout.py`

**Start**

- Under every array there's one long line of bytes. Under every robot there's one long line of code. Mine has a typo.

**After part 1** (Strides and offsets)

- `x.T` just swaps the strides. No data moves. The laziest operation in the world, and I mean that as a compliment.
- `a.T[3, 1, 0]` is `a[0, 1, 3]`. Transposing is just reading the address backwards.

**After part 2** (Contiguity)

- `m.T` isn't contiguous. It jumps around like a robot at a disco.
- `m[1:3]` is contiguous, `m[:, 1:3]` is not. Rows are neighbours, columns are pen pals.

**After part 3** (Strides that repeat)

- broadcast_to made 1000 rows out of 3 numbers. That's not copying, that's recycling.
- Strides (0, 8): a thousand rows, one actual row. The rest is pure confidence.

**After part 4** (🎙️ `c_order_strides` and `is_c_contiguous`)

- You now compute strides the way NumPy does. That makes you an honorary memory manager.
- An array with no elements is always contiguous. Nothing is out of place, because there's nothing.

**Finished**

```
   ____  ____  ____  ____
  | 0  || 1  || 2  || 3  |
  |____||____||____||____|>
   o  o  o  o  o  o  o  o
  "C-contiguous: every wagon right
   behind the last. Pünktlich!"
```

### `e_reshape_and_transpose.py`

**Start**

- Why did the matrix go to the gym? To get into a better shape.

**After part 1** (Reshape or transpose)

- Transpose changes the axes, not the neighbours. Neighbours along each axis stay friends.
- -1 in reshape means "whatever is left". My favourite number at dessert time.

**After part 2** (Shape tools)

- `x.reshape(5, -1)` failed: 12 elements don't fit into 5 rows. Even NumPy can't cut a cake that badly.
- swap_halves: left becomes right, right becomes left. My shoes did that every morning until I labelled them.

**After part 3** (Patches)

- cut_into_patches: a reshape, a transpose, a reshape. A sandwich, and the transpose is the cheese.
- Vision transformers cut images into patches. I cut my puns into patches too. They don't get better.

**After part 4** (`channels_last`, `merge_heads` and `scores_to_vector`)

- channels_last fixed! The pixels stopped mixing their colours. No more rainbow soup.
- A batch of one is lonely enough. Don't squeeze it out of existence.

**Finished**

```
  a = [[0 1 2]    a.reshape(3, 2)    a.T
       [3 4 5]]   [[0 1]             [[0 3]
                   [2 3]              [1 4]
                   [4 5]]             [2 5]]
  "Same shape. Different story."
```

### `f_broadcasting.py`

**Start**

- Broadcasting: when it works, it's magic. When it works by accident, it's a bug.

**After part 1** (Which shapes broadcast)

- (8, 1, 6, 1) + (7, 1, 5) = (8, 7, 6, 5). That's not addition, that's a family reunion.
- np.broadcast_shapes: the dating app that checks if two shapes match before they meet.

**After part 2** (`pairwise_sq_distances`)

- `Y[:, None, :]` instead of `Y[None, :, :]`: one None in the wrong place, and the whole party is cancelled.
- Squared distances: because negative distances would just be rude.

**After part 3** (`mse` and `scale_rows`)

- (N, 1) minus (N,) gives (N, N). You asked for a column and got a whole table. Free upgrade, wrong answer.
- The MSE was always mean. Now it's also correct.

**Finished**

```
     .-------------.
     | RADIO NUMPY |  ((( )))
     | [=]   o  o  |
     |  101.1 FM   |
     '-------------'
  "All shapes, all the time!"
```

### `g_reductions.py`

**Start**

- This puzzle is all about axes. Grab yours, and let's chop some dimensions.

**After part 1** (Which axis disappears)

- `X.sum()` has shape (). The emptiest shape there is. Peak minimalism.
- `np.max(M, 0)` is a reduction, `np.maximum(M, 0)` is ReLU. Four letters apart, one world apart.

**After part 2** (Batch norm and layer norm)

- Batch norm averages over (0, 2, 3), layer norm over (1, 2, 3). One axis apart, and a few research papers.
- Batch norm: one mean per channel. Layer norm: one mean per image. Bender norm: one pun per reply.

**After part 3** (`softmax` and `accuracy`)

- softmax with one global max: one loud row made all the quiet rows vanish. Now every row gets its own max.
- softmax needed its max with keepdims=True. Collapse the axis, keep the memories, as promised.

**Finished**

```
      ____
     /    \____________________
    | AXE  |___________________|  axis=1
     \____/
  "Choose your axis wisely. Chop!"
```

### `h_matmul.py`

**Start**

- Why did the matrix go to therapy? It had inner issues. Its inner sizes didn't match.

**After part 1** (Shapes)

- (3,) @ (3,) gives (). Two vectors walk in, one number walks out.
- `X @ X.T`: every sample compares itself with every other sample. Like social media, but with maths.

**After part 2** (🎙️ `matmul_by_broadcasting`)

- I wrote down your matmul word for word. My keyboard is proud of you.
- row_dots was the warm-up: multiply, then sum. matmul_by_broadcasting is the same song with one more axis.

**After part 3** (`linear` and `attention_scores`)

- Attention scores fixed! Thank you for your attention.
- Square weight matrices hide the (out, in) bug. Square shapes: suspicious since forever.

**Finished**

```
       .---.
      | @ @ |     "I see matrices
      |  -  |      everywhere."
       '---'
       /| |\
```

### `i_forward_pass.py`

**Start**

- Puzzle i: the forward pass. Let's pass forward together. No passing backward until next week.

**After each fixed function** (`shuffle`, `standardize`, `hidden_layer`)

- shuffle: one permutation for X and y. Samples and labels are back together. Love wins.
- standardize: every feature gets its own std now. Fair standards for everyone.
- hidden_layer: max versus maximum strikes again! I saw it coming from puzzle g. So did my screw.

**Finished**

```
   +----------------------------+
   | test loss:     0.2474   OK |
   | test accuracy: 0.9000   OK |
   +----------------------------+
          \(^o^)/   Bender
```

### `j_numpy_to_torch.py`

**Start**

- Puzzle j: from NumPy to PyTorch. Same arrays, new name tag: tensor.

**After part 1** (Same idea, different spelling)

- `t[:, ::-1]` raises an error: PyTorch doesn't do negative steps. Very positive library.
- NumPy counts strides in bytes, PyTorch in elements. One is an accountant, the other a mathematician.

**After part 2** (Who shares memory)

- from_numpy shares memory, torch.tensor copies. One moves in together, the other just keeps a photo.
- `a[0]` became 11 in three places at once. Shared memory: the group chat of arrays.

**After part 3** (`view`, `reshape` and `contiguous`)

- view refuses non-contiguous tensors. PyTorch likes its memory in a neat line, thank you very much.
- `t.T.contiguous().view(12)`: first you tidy up, then you get your view.

**After part 4** (Naive ports)

- torch.maximum wants two tensors. The zero had to dress up as `torch.zeros_like(x)` to get in.
- `x.flip(1)` instead of `x[:, ::-1]`: PyTorch reverses time, but only politely.

**Finished**

```
        (  )
       (    )
        )  (
       [====]
        |  |     torch
        |  |     "NumPy, now with
        |  |      a flame."
        |__|
```
