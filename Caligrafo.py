#! /usr/bin/python3

#	Caligrafo.py

''' Enzo Zavorski Delevatti
||| @Zvorky
\\\          ___,
 \\\      .~´    `-,
  \\°    /  _    _ \.
   \°   ,\`|_|''|_|´\
    °    /          /)   °
        (\  ,    , .\`   |°
         `) ;`,; `,^,)   ||°
         ´,´  `,  `  `   |||
                          \\\
         July    2023      |||
                           '''



import os



class Margin:
    def __init__(self, paragraph = 0, left = 0, right = 0, top = 0, bottom = 0):
        self.paragraph = paragraph
        self.left   = left
        self.right  = right
        self.top    = top
        self.bottom = bottom
    

    #   Set margin spacing values, None = Set all 0. "amount" have minor priority.
    def Set(self, left: int | None = None, right: int | None = None, top: int | None = None, bottom: int | None = None, amount: int | None = 0):
        if(amount < 0):
            return False
        
        # Reset / Set All 0
        if(left == None and right == None and top == None and bottom == None):
            self.left = self.right = self.top = self.bottom = amount
            return True
        
        values = [left, right, top, bottom]

        # Check Values
        for value in values:
            if(value != None and value < 0):
                return False
        
        # Set Values
        if(left != None):
            self.left = left

        if(right != None):
            self.right = right
        
        if(top != None):
            self.top = top
        
        if(bottom != None):
            self.bottom = bottom

        return True
    

    def SetParagraph(self, amount: int):
        if(amount < 0):
            return False
        self.paragraph = amount
        return True
    

    def CenterMargin(self):
        self.left = self.right = (self.left + self.right) / 2
        self.top = self.bottom = (self.top + self.bottom) / 2



class Alignment:
    # Index 0 represents default alignment
    Horizontals = ['left', 'center', 'right', 'justified']
    Verticals = ['top', 'center', 'bottom']


    def __init__(self, horizontal: str | None = 'left', vertical: str | None = 'top'):
        self.horizontal = Alignment.Horizontals[0]
        self.vertical = Alignment.Verticals[0]
    
    
    #   None = Reset Default (Top Left). Horizontal = left; center; right; justified. Vertical = top; center; bottom.
    def Set(self, horizontal: str | None = '', vertical: str | None = ''):
        # Resets
        if(not horizontal and not vertical):
            horizontal = Alignment.Horizontals[0]
            vertical = Alignment.Verticals[0]

        horizontal = horizontal.lower() if horizontal else self.horizontal
        vertical = vertical.lower() if vertical else self.vertical
        
        if(not horizontal in Alignment.Horizontals or not vertical in Alignment.Verticals):
                return False
        
        self.horizontal = horizontal
        self.vertical = vertical
            
        return True
    

    def ApplyHorizontal(self, text: str, width: int):
        if(self.horizontal == 'left'):
            return text
        
        string = ''
        lines = text.splitlines()
        
        # Apply
        for line in lines:
            if(self.horizontal == 'right'):
                string += ' ' * (width - len(line)) + line
            elif(self.horizontal == 'center'):
                spacing = int((width - len(line)) / 2)
                string += ' ' * spacing + line + ' ' * spacing
            else: # Justified
                words = line.split()

                letters = 0
                for word in words:
                    letters += len(word)
                
                spacing = []
                for i in range(len(words)-1):
                    spacing.append(int((width - letters) / (len(words))))
                    # print(letters, width - letters, int((width-letters)/len(words)))
                
                i = 0
                while(sum(spacing) + letters < width):
                    spacing[i] += 1
                    i += 1
                    if(i >= len(spacing)):
                        i = 0
                
                for i in range(len(spacing)):
                    string += words[i] + ' ' * spacing[i]
                
                string += words[len(words)-1]
            
            string += '\n'
        
        return string[:-1]



class TextBox:
    def __init__(self, text = '', width = 0, height = 0, margin = Margin(), alignment = Alignment(), limitMsg = '[...]'):
        self.text = text
        self.width = width
        self.height = height
        self.margin = margin
        self.alignment = alignment
        self.limitMsg = limitMsg
    

    #   None = Reset Default (Top Left). Horizontal = left; center; right; justified. Vertical = top; center; bottom.
    def SetAlignment(self, horizontal: str | None = '', vertical: str | None = ''):
        return(self.alignment.Set(horizontal, vertical))
    

    #   Set margin spacing values, None = Set All 0. "amount" have minor priority.
    def SetMargin(self, left: int | None = None, right: int | None = None, top: int | None = None, bottom: int | None = None, amount: int | None = 0):
        horizontal = vertical = 0
        
        if(left != None):
            horizontal += left
        if(right != None):
            horizontal += right
        
        if(top != None):
            vertical += top
        if(bottom != None):
            vertical += bottom
        
        if(not horizontal and not vertical):
            horizontal = vertical = amount
        
        # Size consistency
        if(self.width and horizontal >= self.width):
            return False
        if(self.height and vertical >= self.height):
            return False
        
        return self.margin.Set(left, right, top, bottom, amount)
    

    def SetParagraph(self, amount: int):
        return self.margin.SetParagraph(amount)
    

    #   Return a reduced paragraph margin if width is too small
    def GetParagraph(self):
        if(self.width > 0 and self.margin.paragraph >= self.width):
            return self.width-1
        else:
            return self.margin.paragraph
    

    def CenterMargin(self):
        self.margin.CenterMargin()
    

    #   Set Size
    def Resize(self, width: int | None = 0, height: int | None = 0):
        if(width < 0 or height < 0):
            return False
        
        # Margin consistency
        if(width and width <= self.margin.left + self.margin.right):
            return False
        
        if(height and height <= self.margin.top + self.margin.bottom):
            return False
        
        self.width = width
        self.height = height

        return True
    
    
    def MaxWidth(self):
        if(self.width):
            return self.width
        
        margin = self.GetParagraph() + self.margin.left + self.margin.right

        max = 0
        column = margin
        for char in self.text:
            if(char == '\n'):
                column = margin
            else:
                column += 1
            
            if(column > max):
                max = column
        return max
    

    #   Return a tuple with Max Width and Height
    def Size(self):
        width = self.width
        height = self.height

        if(width and height):
            return width, height

        paragraph = self.GetParagraph()

        column = 1 # Number of Columns in current Line
        line   = 1 # Number of Lines in current String

        # Top Margin
        line += self.margin.top

        newline = False
        newparagraph = True
        for char in self.text:

            # Paragraph Margin
            if(newparagraph):
                newparagraph = False
                column = paragraph + self.margin.left

            column += 1

            # New Line into Paragraph
            if(char == '\n'):
                char = ''
                column += self.margin.right - 1
                newline = True
                newparagraph = True

            # Width Limit into New Line
            elif(column == self.width - self.margin.right):
                column += self.margin.right
                newline = True

            if(column > width):
                width = column

            # Check Limit and add New Line
            if(newline):
                newline = False

                # Height Limit
                if(line == self.height - self.margin.bottom):
                    height += self.margin.bottom
                    return width, height

                column = self.margin.left + 1
                line   += 1
            
            if(line > height):
                height = line

        # Bottom Margin
        if(not self.height):
            height += self.margin.bottom

        return width, height
    
    
    #   Return the text with the formatting applied
    def __str__(self):
        string = ''

        paragraph = self.GetParagraph()
        width, height = self.Size()

        column = paragraph  # Number of Columns in current Line
        line   = 1          # Number of Lines in current String

        # Top Margin
        line += self.margin.top
        string += '\n' * self.margin.top
        
        # Initial Left Margin
        string += ' ' * self.margin.left

        newline = False
        newparagraph = True
        for char in self.text:
            
            # Paragraph Margin
            if(newparagraph):
                newparagraph = False
                string += ' ' * paragraph
                column = paragraph + self.margin.left
            
            # New Line to Paragraph
            if(char == '\n'):
                char = ''
                newline = True
                newparagraph = True
            
            # Width Limit to New Line
            elif(column == width - self.margin.right):
                newline = True
            
            else:
                string += char
                column += 1
            
            # Check Limit and add New Line
            if(newline):
                newline = False

                # Height Limit
                if(line == height - self.margin.bottom):

                    # Remove Paragraph or all Text if needed
                    if(len(string) <= len(self.limitMsg) + paragraph):
                        if(len(string) <= len(self.limitMsg)):
                            string = ''
                        else:
                            string = string[paragraph:-1]
                    
                    # Fills the Text Box with spaces
                    else:
                        if(width):
                            string += ' ' * (width - column)
                            string = string[0:len(string) - len(self.limitMsg)]
                    
                    if(len(self.limitMsg) > width and line > 1):
                        string += '\n'
                    
                    string += self.limitMsg
                    
                    # Bottom Margin
                    string += '\n' * self.margin.bottom
                        
                    return string
                
                # Add Newline
                string += '\n' + ' ' * self.margin.left + char
                column = self.margin.left + 1
                line   += 1
        
        # Top Alignment = do nothing

        # Center Alignment
        if(self.alignment.vertical == 'center'):
            string = '\n' * int((height - line - self.margin.bottom) / 2) + string
            line += int((height - line - self.margin.bottom) / 2)
        
        # Bottom Alignment
        elif(self.alignment.vertical == 'bottom'):
            string = '\n' * (height - line - self.margin.bottom) + string
            line += height - line - self.margin.bottom
        
        # Bottom Margin
        string += '\n' * (height - line)

        string = self.alignment.ApplyHorizontal(string, width)

        return string



if __name__ == '__main__':
    test = TextBox(
'''▒███████▒ ██▒   █▓ ▒█████   ██▀███   ██ ▄█▀▓██   ██▓
▒ ▒ ▒ ▄▀░▓██░   █▒▒██▒  ██▒▓██ ▒ ██▒ ██▄█▒  ▒██  ██▒
░ ▒ ▄▀▒░  ▓██  █▒░▒██░  ██▒▓██ ░▄█ ▒▓███▄░   ▒██ ██░
  ▄▀▒   ░  ▒██ █░░▒██   ██░▒██▀▀█▄  ▓██ █▄   ░ ▐██▓░
▒███████▒   ▒▀█░  ░ ████▓▒░░██▓ ▒██▒▒██▒ █▄  ░ ██▒▓░
░▒▒ ▓░▒░▒   ░ ▐░  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▒ ▓▒   ██▒▒▒ 
░░▒ ▒ ░ ▒   ░ ░░    ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒ ▒░ ▓██ ░▒░ 
░ ░ ░ ░ ░     ░░  ░ ░ ░ ▒    ░░   ░ ░ ░░ ░  ▒ ▒ ░░  
  ░ ░          ░      ░ ░     ░     ░  ░    ░ ░     
░             ░                             ░ ░     ''')
    test.Resize(int(input('width:')), int(input('height:')))
    # test.SetParagraph(int(input('paragraph:')))
    # test.SetMargin(int(input('Margin\nLeft:')), int(input('Right:')), int(input('Top:')), int(input('Bottom:')))
    # test.SetAlignment(input('Alignment\nHorizontal:'), input('Vertical:'))

    for i in range(test.MaxWidth()):
        if((i+1)%10):
            print('_', end='')
        else:
            print(int((i+1)/10), end='')
    print('')
    
    for i in range(test.MaxWidth()):
        print((i+1)%10, end='')
    print('')
    
    # print(str(test))
    print(test.Size())

    test.SetAlignment('justified')
    print(str(test))