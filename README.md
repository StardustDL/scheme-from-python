# ![scheme-from-python](https://socialify.git.ci/StardustDL/scheme-from-python/image?description=1&font=Bitter&forks=1&issues=1&language=1&owner=1&pulls=1&stargazers=1&theme=Light "scheme-from-python")

[![](https://github.com/StardustDL/scheme-from-python/workflows/CI/badge.svg)](https://github.com/StardustDL/scheme-from-python/actions) [![](https://img.shields.io/github/license/StardustDL/scheme-from-python.svg)](https://github.com/StardustDL/coxbuild/blob/master/LICENSE)
<!--[![](https://img.shields.io/pypi/v/scheme-from-python)](https://pypi.org/project/scheme-from-python/) [![Downloads](https://pepy.tech/badge/scheme-from-python?style=flat)](https://pepy.tech/project/scheme-from-python)-->

[scheme-from-python](https://github.com/StardustDL/scheme-from-python) is an experimental scheme interpreter in Python.

https://user-images.githubusercontent.com/34736356/193305337-c5a48c83-2d31-4a46-9ff8-370619967530.mov

- Scheme core
  - [x] define
  - [x] if
  - [x] lambda (with closures)
- Builtin functions
  - [x] Boolean operators
  - [x] Arithmetic operators (integer, float, complex)
  - [x] Comparing operators
- Interoperation
  - [x] Auto signature inferring from Python to Scheme
  - [x] Lazy or non-lazy functions
  - [x] Capturing the evaluation context (symbol table)
- Interpreter
  - [x] File / command-line expression
  - [x] Auto-indented multi-line
  - [x] Auto fixing missing right parentheses


> For sequence expression, the final value is the value of the last sub-expression, e.g., `1 2 3` = `3`.

## Values

- Boolean: `#t` true, `#f` false
- Integer: `0`, `-1`, `2`, ...
- Float: `0.1`, `1.5`, ...
- Complex: `1+2j`, `3+4j`, ...
- Symbol: `a`, `b`, `c`, `+`, `-`, ...
- Function: `(lambda (x) (+ x 1))`, ...
- Empty: `<empty>` only as return value

## Builtins

### Core

**`(define symbol_name value_expression)`**

Define a symbol with exact value, and return the symbol, `def` for a short alternative.

**`(if predicate_expression true_expression false_expresion)`**

Branch expression, if `predicate_expression` is not `#f`, then evaluate and return the value of `true_expression`, otherwise evaluate and return the value of `false_expression`.

**`(lambda (p1 p2 ... pn) body_expression`**

Lambda expresion, define an anonymous function (closure) with the parameters named `p1`, `p2`, ..., `pn` (can be empty, i.e., `()`), and the function body, `lam` for a short alternative.

The lambda function creates a sub-symbol-table, so `define` in a lambda function can only write current symbols, and cannot write upstream symbols (can hidden them by define symbols in the same name). Here is an example code snippet.

```scheme
>>> ((lambda () (define x 1)))
x
>>> x
Undefined symbol: x
```

### Boolean

**`(not b)`**

$$=\neg b$$

**`(and b1 b2 ... bn)`** *without short circuit*

$$=\bigwedge_{i=1}^n b_i$$

**`(or b1 b2 ... bn)`** *without short circuit*

$$=\bigvee_{i=1}^n b_i$$

### Arithmetic

The operands must be integers.

**`(+ v1 v2 ... vn)`**

$$=\sum_{i=1}^n v_i$$

**`(- v1 v2)`**

$$=v_1 - v_2$$

**`(* v1 v2 ... vn)`**

$$=\prod_{i=1}^n v_i$$

**`(// v1 v2)`**

$$=\lfloor v_1 / v_2 \rfloor$$

**`(/ v1 v2)`**

$$=v_1 / v_2$$

**`(% v1 v2)`**

$$=v_1 \% v_2$$

**`(^ v1 v2)`**

$$=v_1^{v_2}$$

**`(max v1 v2 ... vn)`**

$$=\max_{i=1}^n v_i$$

**`(min v1 v2 ... vn)`**

$$=\min_{i=1}^n v_i$$

### Comparing

**`(< v1 v2)`**

$$=\textbf{boolean}(v_1 < v_2)$$

**`(<= v1 v2)`**

$$=\textbf{boolean}(v_1 \le v_2)$$

**`(> v1 v2)`**

$$=\textbf{boolean}(v_1 > v_2)$$

**`(>= v1 v2)`**

$$=\textbf{boolean}(v_1 \ge v_2)$$

**`(= v1 v2)`**

$$=\textbf{boolean}(v_1 = v_2)$$

**`(!= v1 v2)`**

$$=\textbf{boolean}(v_1 \ne v_2)$$

### Input / Output

**`(print v)`**

Print the value and return empty.

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

python -m sfpy -f ./demo/arithmetic.scm
python -m sfpy -f ./demo/lambda.scm
python -m sfpy -f ./demo/factorial.scm
```
