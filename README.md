# PEMDASParsing
A small script to generate binary syntax trees out of arithmetic expressions and evaluate them to floats.

Entrypoints to this module are
+ `parse` - takes a string and returns a Binary Syntax Tree chosen via PEMDAS
+ `evaluate_string` - takes a string and returns a float evaluated by PEMDAS

The intermediate stage (binary syntax tree) isn't necessary for PEMDAS evaluation;
I included it to demonstrate that order of operations (in general *all* ambiguous
grammar evaluation strategies) are just about algorithmically picking a syntax tree
for an expression.

Strategy to find syntax tree:
- Break string into top level tokens (operations, numbers, bracket expressions)
- Fold top level token list into binary tree, starting from the leftmost, lowest
  precedence operation, going right to left then up precedence.
- When a bracket expression is encountered, the outermost brackets are removed
  and the inner expression is parsed.