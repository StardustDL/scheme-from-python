# scheme-from-python

An experimental scheme interpreter in Python.

- Scheme core
  - [ ] define
  - [ ] lambda
- Builtin functions
  - [x] Arithmestic operators for integers

## Functions

### Arithmestic

The operands must be integers.

- `(+ v1 v2 ... vn)` $=\sum_{i=1}^n v_i$
- `(- v1 v2)` $=v_1 - v_2$
- `(* v1 v2 ... vn)` $=\prod_{i=1}^n v_i$
- `(/ v1 v2)` $=\lfloor v_1 / v_2 \rfloor$
- `(^ v1 v2)` $=v_1^{v_2}$

## Install

```sh
conda create -n sfpy python=3.10
conda activate sfpy
cd src
pip install -r requirements.txt
```

## Usage

sfpy supports interactor (for user input) and interpreter (for file input) mode.

### Interactor Mode

```sh
python -m sfpy
```

### Interpreter Mode

```sh
python -m sfpy -f your_scheme_file

python -m sfpy -e "your scheme expression"

# an arithmestic demo
python -m sfpy -e "(+ (* 1 1) (- 3 2) (^ 2 0) (/ 4 4))"
python -m sfpy -f ../demo/arithmestic.scm
```