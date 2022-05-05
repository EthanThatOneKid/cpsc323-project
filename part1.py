#!/usr/bin/python
# Name: part1cpsc323.py
# Authors: Karnikaa Velumani, Ethan Davidson

txt = open('finalp1.txt')
f = open('finalp2.txt', 'w')

(ASTERISK, SLASH, EMPTY_SPACE) = ('*', '/', ' ')
START_COMMENT = SLASH + ASTERISK
END_COMMENT = ASTERISK + SLASH

def rid_whole_comments(line):
    opening_index = line.find(START_COMMENT)
    while opening_index > -1:
        closing_index = line.find(END_COMMENT, opening_index)
        if closing_index == -1:
            break
        line_before_comment = line[0:opening_index]
        line_after_comment = line[closing_index
            + len(END_COMMENT):len(line)]
        line = line_before_comment + line_after_comment  # Remove whole comment from line.
        opening_index = line.find(START_COMMENT)
    return line

def rid_consecutive_spaces(line):
    result = ""
    for i in range(len(line)):
        if i > 0 and line[i] == EMPTY_SPACE and line[i-1] == EMPTY_SPACE:
            continue
        result += line[i]
    return result

# Read first line in input program
line = txt.readline()
comment_is_happening = False
while len(line):

    # Removes blank lines
    if line != '\n':

        # Remove end of multiline comment
        end_comment_index = line.find(END_COMMENT)
        if comment_is_happening and end_comment_index > -1:
            line_after_comment = line[end_comment_index
                + len(END_COMMENT):len(line)]
            line = line_after_comment
            comment_is_happening = False
        elif comment_is_happening:

            # Read next line in input program
            line = txt.readline()
            continue

        line = rid_whole_comments(line)

        # Remove start of multiline comment
        start_comment_index = line.find(START_COMMENT)
        if not comment_is_happening and start_comment_index > -1:
            line_before_comment = line[0:start_comment_index]
            line = line_before_comment
            comment_is_happening = True

        # Remove spaces in the beginning of the string
        line = line.lstrip()

        # Remove consecutive spaces
        line = rid_consecutive_spaces(line)

        # Removes empty lines
        if line == '':

            # Read next line in input program
            line = txt.readline()
            continue

        f.write(line)

    # Read next line in input program
    line = txt.readline()