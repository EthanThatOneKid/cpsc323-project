#!/usr/bin/python
# Project: CPSC 323 Part 2
# Authors: Karnikaa Velumani, Ethan Davidson

# Tokenization
LITERAL_PROGRAM = "program"
LITERAL_VAR = "var"
LITERAL_BEGIN = "begin"
LITERAL_END = "end"
LITERAL_INTEGER = "integer"
LITERAL_WRITE = "write"
LITERAL_COLON = ":"
LITERAL_SEMICOLON = ";"
LITERAL_OPEN_PARENTHESIS = "("
LITERAL_CLOSE_PARENTHESIS = ")"
LITERAL_QUOTE = "\""
LITERAL_PERIOD = "."
LITERAL_COMMA = ","
LITERAL_SPACE = " "
LITERAL_EQUAL = "="
LITERAL_ADDITION = "+"
LITERAL_SUBTRACTION = "-"
LITERAL_MULTIPLICATION = "*"
LITERAL_DIVISION = "/"

class Token:
  def debug(self):
    # if hasattr(self, "keyword"): print(self.keyword)
    # elif hasattr(self, "id"): print(self.id)
    # elif hasattr(self, "sign"): print(self.sign)
    # elif hasattr(self, "marking"): print(self.marking)
    # elif hasattr(self, "content"): print(self.content)
    pass
  
  def vdebug(self):
    if hasattr(self, "keyword"): print(f"keyword: '{self.keyword}'.")
    elif hasattr(self, "id"): print(f"id: '{self.id}'.")
    elif hasattr(self, "sign"): print(f"sign: '{self.sign}'.")
    elif hasattr(self, "marking"): print(f"marking: '{self.marking}'.")
    elif hasattr(self, "content"): print(f"content: '{self.content}'.")

class KeywordToken(Token):
  KEYWORDS = {
    LITERAL_PROGRAM,
    LITERAL_VAR,
    LITERAL_BEGIN,
    LITERAL_END,
    LITERAL_INTEGER,
    LITERAL_WRITE
  }
  def __init__(self, keyword: str):
    self.keyword = keyword

class IdentifierToken(Token):
  def __init__(self, id: str):
    self.id = id

class DigitsToken(Token):
  def __init__(self, digits: str):
    self.digits = digits

class CustomStringToken(Token):
  def __init__(self, content: str):
    self.content = content

class SignToken(Token):
  SIGNS = {
    LITERAL_ADDITION,
    LITERAL_SUBTRACTION,
    LITERAL_MULTIPLICATION,
    LITERAL_DIVISION
  }
  def __init__(self, sign: str):
    self.sign = sign

class PunctuationToken(Token):
  MARKINGS = {
    LITERAL_COLON,
    LITERAL_SEMICOLON,
    LITERAL_OPEN_PARENTHESIS,
    LITERAL_CLOSE_PARENTHESIS,
    LITERAL_PERIOD,
    LITERAL_COMMA,
    LITERAL_EQUAL
  }
  def __init__(self, marking: str):
    self.marking = marking

def tokenize(program: str):
  tokens = []
  curr_tok = ""
  tok_is_numeric = False
  tok_is_string = False
    
  for i in range(len(program)):
    curr_char = program[i]

    if tok_is_string:
      if curr_char == LITERAL_QUOTE:
        tokens.append(CustomStringToken(curr_tok))
        tok_is_string = False
        curr_tok = ""
        continue
      else:
        curr_tok += curr_char
        continue
    
    char_code = ord(curr_char)

    # chr(48) == "0" and chr(57) == "9"
    is_digit = 48 <= char_code and char_code <= 57

    # chr(65) == "A" and chr(90) == "Z" and \
    # chr(97) == "a" and chr(122) == "z"
    is_upper = 65 <= char_code and char_code <= 90
    is_lower = 97 <= char_code and char_code <= 122

    is_alphanum = is_upper or is_lower or is_digit
    if (is_digit and tok_is_numeric) or \
       (is_alphanum and not tok_is_numeric):
      if is_digit and len(curr_tok) == 0: tok_is_numeric = True
      curr_tok += curr_char
      continue

    if len(curr_tok) > 0: # Reset token
      is_keyword = curr_tok in KeywordToken.KEYWORDS
      if tok_is_string: tokens.append(CustomStringToken(curr_tok))
      elif is_keyword: tokens.append(KeywordToken(curr_tok))
      elif curr_tok.isdecimal(): tokens.append(DigitsToken(curr_tok))
      else: tokens.append(IdentifierToken(curr_tok))
      tok_is_numeric = False
      tok_is_string = False
      curr_tok = ""

    if curr_char == LITERAL_QUOTE:
      tok_is_string = True
      continue

    if curr_char in PunctuationToken.MARKINGS:
      tokens.append(PunctuationToken(curr_char))
      continue

    if curr_char in SignToken.SIGNS:
      tokens.append(SignToken(curr_char))
      continue

  return tokens

class State:
  pass

class DeclarationState(State):
  def __init__(self, id: IdentifierToken):
    self.id = id
    
class DecListState(State):
  def __init__(self):
    self.declarations = []
    self.type_name = KeywordToken(LITERAL_INTEGER)
  def set_type_name(self, type_name: KeywordToken):
    self.type_name = type_name
  def append_dec(self, dec: DeclarationState):
    self.declarations.append(dec)
  def set_decs(self, decs: list[DeclarationState]):
    self.declarations = decs
  def debug(self):
    print(f"DecListState({self.type_name.keyword})")
  
class TypeState(State):
  def __init__(self, type_name: KeywordToken):
    self.type_name = type_name

class WriteState(State):
  def __init__(self):
    self.custom_string = None
    self.id = None
  def set_id(self, id: IdentifierToken):
    self.id = id
  def set_custom_string(self, custom_string: CustomStringToken):
    self.custom_string = custom_string

class NumberState(State):
  def __init__(self):
    self.sign = None
    self.digits = None
  def set_sign(self, sign: SignToken):
    self.sign = sign
  def set_digits(self, digits: DigitsToken):
    self.digits = digits

class FactorState(State):
  def __init__(self):
    self.id = None # Either this one
    self.num = None # Or that one
    self.expression = None # Or even that one
    # (One is populated while the others are None)
  def set_id(self, id: IdentifierToken):
    self.id = id
  def set_num(self, num: NumberState):
    self.num = num
  def set_expression(self, expression: 'ExpressionState'):
    self.expression = expression

class TermState(State):
  def __init__(self):
    self.factor = None
    self.sign = None # * or /
    self.term = None
  def set_factor(self, factor: FactorState):
    self.factor = factor
  def set_sign(self, sign: SignToken):
    self.sign = sign
  def set_term(self, term: 'TermState'):
    self.term = term

class ExpressionState(State):
  def __init__(self):
    self.expression = None
    self.sign = None # + or -
    self.term = None
  def set_expression(self, expr: 'ExpressionState'):
    self.expression = expr
  def set_sign(self, sign: SignToken):
    self.sign = sign
  def set_term(self, term: TermState):
    self.term = term

class AssignState(State):
  def __init__(self):
    self.id = None
    self.expression = None
  def set_id(self, id: IdentifierToken):
    self.id = id
  def set_expression(self, expression: ExpressionState):
    self.expression = expression

class StatementState(State):
  def __init__(self):
    self.write = None # Either this one
    self.assign = None # Or that one
    # (One is populated while the other is None)
  def set_write(self, write: WriteState):
    self.write = write
  def set_assign(self, assign: AssignState):
    self.assign = assign

class StatListState(State):
  def __init__(self):
    self.statements = []
  def append_stat(self, statement: StatementState):
    self.statements.append(statement)

class ExprListState(State):
  def __init__(self):
    self.expressions = []
  def append_expression(self, expression: ExpressionState):
    self.expressions.append(expression)

class ProgramState(State):
  def set_id(self, id: IdentifierToken):
    self.id = id
  def set_dec_list(self, dec_list: DecListState):
    self.dec_list = dec_list
  def set_stat_list(self, stat_list: StatListState):
    self.stat_list = stat_list
  def debug(self):
    print(f"ProgramState({self.id.id})")
    # self.dec_list.debug()
    # self.stat_list.debug()

class CustomStringState(State):
  def __init__(
    self,
    custom_string: CustomStringToken,
    id: IdentifierToken
  ):
    self.custom_string = custom_string
    self.id = id

def print_cpsc323error(wanted: str = ""):
  if wanted in KeywordToken.KEYWORDS:
    print(wanted + " is expected")
  elif wanted in PunctuationToken.MARKINGS:
    print(wanted + " is missing")
  else:
    print("unknown identifier")

def eat(toks: list[Token]) -> tuple[Token, list[Token]]:
  if len(toks) > 0:
    next_token = toks[0]
    return next_token, toks[1:]
  return (), []

def consume_write(toks: list[Token]) -> tuple[WriteState, list[Token]]:
  write_state = WriteState()

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_OPEN_PARENTHESIS
  if not is_ok:
    print_cpsc323error(LITERAL_OPEN_PARENTHESIS)
    return None, toks
    
  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, CustomStringToken)
  if not is_ok:
    print_cpsc323error()
    return None, toks
  write_state.set_custom_string(curr_tok)

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_COMMA
  if not is_ok:
    print_cpsc323error(LITERAL_COMMA)
    return None, toks

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, IdentifierToken)
  if not is_ok:
    print_cpsc323error()
    return None, toks
  write_state.set_id(curr_tok)

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_CLOSE_PARENTHESIS
  if not is_ok:
    print_cpsc323error(LITERAL_CLOSE_PARENTHESIS)
    return None, toks

  return write_state

def consume_expression(toks: list[Token]) -> tuple[ExpressionState, list[Token]]:
  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_id = isinstance(curr_tok, IdentifierToken)
  is_num = isinstance(curr_tok, NumberState)
  is_open_paren = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_OPEN_PARENTHESIS
  is_ok = is_id or is_num or is_open_paren
  if not is_ok:
    print_cpsc323error()
    return None, toks

def consume_assign(toks: list[Token], id: IdentifierToken) -> tuple[AssignState, list[Token]]:
  assign_state = AssignState()
  assign_state.set_id(id)
  
  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_EQUAL
  if not is_ok:
    print_cpsc323error(LITERAL_EQUAL)
    return None, toks

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_EQUAL
  if not is_ok:
    print_cpsc323error(LITERAL_EQUAL)
    return None, toks
  
  expression, toks = consume_expression(toks)
  is_ok = expression is not None
  if not is_ok:
    return None, toks
  assign_state.set_expression(expression)

  return assign_state, toks

def consume_stat_list(toks: list[Token]) -> tuple[StatListState, list[Token]]:
  stat_list = StatListState()

  while True:
    curr_stat = StatementState()
    curr_tok, toks = eat(toks)
    is_write = isinstance(curr_tok, KeywordToken) and curr_tok.keyword == LITERAL_WRITE
    is_assign = isinstance(curr_tok, IdentifierToken)
    is_ok = is_write or is_assign
    if not is_ok:
      print_cpsc323error()
      return None, toks
    
    if is_write:
      write_state, toks = consume_write(toks)
      is_ok = write_state is not None
      if not is_ok:
        print_cpsc323error()
        return None, toks
      curr_stat.set_write(write_state)
    elif is_assign:
      assign_state, toks = consume_assign(toks, curr_tok)
      is_ok = assign_state is not None
      if not is_ok:
        print_cpsc323error()
        return None, toks
      curr_stat.set_assign(assign_state)
    
    # Consume semicolon
    curr_tok, toks = eat(toks)
    is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_SEMICOLON
    if not is_ok:
      print_cpsc323error(LITERAL_SEMICOLON)
      return None, toks

    return stat_list, toks

def consume_dec_list(toks: list[Token]) -> tuple[DecListState, list[Token]]:
  dec_list = DecListState()

  while True:
    curr_tok, toks = eat(toks)
    is_ok = isinstance(curr_tok, IdentifierToken)
    if not is_ok:
      print_cpsc323error()
      return None, toks
    curr_tok.debug()
    dec = DeclarationState(curr_tok)
    dec_list.append_dec(dec)

    curr_tok, toks = eat(toks)
    curr_tok.debug()
    is_done = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_COLON
    if is_done:
      break

    is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_COMMA
    if not is_ok:
      print_cpsc323error(LITERAL_COMMA)
      return None, toks

  curr_tok, toks = eat(toks)
  is_ok = isinstance(curr_tok, KeywordToken)
  if not is_ok:
    print_cpsc323error(LITERAL_INTEGER)
    return None, toks
  dec_list.set_type_name(curr_tok)

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_SEMICOLON
  if not is_ok:
    print_cpsc323error(LITERAL_SEMICOLON)
    return None, toks

  return dec_list, toks

# Construct the AST (Abstract Syntax Tree) from the list of tokens.
def consume_program(toks: list[Token]) -> ProgramState:
  program = ProgramState()
  
  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, KeywordToken) and curr_tok.keyword == LITERAL_PROGRAM
  if not is_ok:
    print_cpsc323error(LITERAL_PROGRAM)
    return program

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, IdentifierToken)
  if not is_ok:
    print_cpsc323error()
    return program
  program.set_id(curr_tok)

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_SEMICOLON
  if not is_ok:
    print_cpsc323error(LITERAL_SEMICOLON)
    return program

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, KeywordToken) and curr_tok.keyword == LITERAL_VAR
  if not is_ok:
    print_cpsc323error(LITERAL_VAR)
    return program

  dec_list, toks = consume_dec_list(toks)
  is_ok = dec_list is not None
  if not is_ok:
    return program
  program.set_dec_list(dec_list)

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, KeywordToken) and curr_tok.keyword == LITERAL_BEGIN
  if not is_ok:
    print_cpsc323error(LITERAL_BEGIN)
    return program

#   Un-Comment this to consume statements
#   stat_list, toks = consume_stat_list(toks)
#   is_ok = stat_list is not None
#   if not is_ok:
#     return program
#   program.set_stat_list(stat_list)
    
  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, KeywordToken) and curr_tok.keyword == LITERAL_END
  if not is_ok:
    print_cpsc323error(LITERAL_END)
    return program

  curr_tok, toks = eat(toks)
  curr_tok.debug()
  is_ok = isinstance(curr_tok, PunctuationToken) and curr_tok.marking == LITERAL_PERIOD
  if not is_ok:
    print_cpsc323error(LITERAL_PERIOD)
    return program

  return program

sample_code1 = """program a2022;
va
a1 , b2a,  wc, ba12 : integer;
begin
end."""

# sample_code2 = """program a2022;
# var
# a1 , b2a , wc, ba12 : integer;
# begin
# a1 = 3;
# b2a = 4;
# wc = 5 ;
# write(wc ); 
# ba12 = a1 * (b2a + 2 * wc)
# write("value=", ba12 ); 
# end."""

toks = tokenize(sample_code1)
program = consume_program(toks)
program.debug()