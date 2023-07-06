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



class Spacing:
    def __init__(self, paragraph = 0, left = 0, right = 0, top = 0, bottom = 0):
        self.paragraph = paragraph
        self.left   = left
        self.right  = right
        self.top    = top
        self.bottom = bottom
    

    #   Set margin spacing values, None = Set all 0. "amount" have minor priority.
    def SetMargin(self, left: int | None = None, right: int | None = None, top: int | None = None, bottom: int | None = None, amount: int | None = 0):
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



class TextBox:
    def __init__(self, text = '', width = 0, height = 0, limitMsg = '[...]'):
        self.text = text
        self.width = width
        self.height = height
        self.spacing = Spacing()
        self.alignH = 'left'
        self.alignV = 'top'
        self.limitMsg = limitMsg
    

    #   None = Reset Default (Top Left). Horizontal = left; center; right; justified. Vertical = top; center; bottom.
    def SetAlignment(self, horizontal: str | None = '', vertical: str | None = ''):
        # Resets
        if(not horizontal and not vertical):
            horizontal = 'left'
            vertical = 'top'

        horizontal = horizontal.lower() if horizontal else self.alignH
        vertical = vertical.lower() if vertical else self.alignV
        
        if(horizontal != 'left' and horizontal != 'center' and horizontal != 'right' and horizontal != 'justified'):
                return False
        if(vertical != 'top' and vertical != 'center' and vertical != 'bottom'):
                return False
        
        self.alignV = vertical
        self.alignH = horizontal
            
        return True
    

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
        
        return self.spacing.SetMargin(left, right, top, bottom, amount)
    

    def SetParagraph(self, amount: int):
        return self.spacing.SetParagraph(amount)
    

    # Return a reduced paragraph spacing if width is too small
    def GetParagraph(self):
        if(self.width > 0 and self.spacing.paragraph >= self.width):
            return self.width-1
        else:
            return self.spacing.paragraph
    

    def CenterMargin(self):
        self.spacing.CenterMargin()
    

    #   Set Size
    def Resize(self, width: int | None = 0, height: int | None = 0):
        if(width < 0 or height < 0):
            return False
        
        # Margin consistency
        if(width and width <= self.spacing.left + self.spacing.right):
            return False
        
        if(height and height <= self.spacing.top + self.spacing.bottom):
            return False
        
        self.width = width
        self.height = height

        return True
    
    
    def MaxWidth(self):
        if(self.width):
            return self.width
        
        spacing = self.GetParagraph() + self.spacing.left + self.spacing.right

        max = 0
        column = spacing
        for char in self.text:
            if(char == '\n'):
                column = spacing
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
        line += self.spacing.top

        newline = False
        newparagraph = True
        for char in self.text:

            # Paragraph Spacing
            if(newparagraph):
                newparagraph = False
                column = paragraph + self.spacing.left

            column += 1

            # New Line into Paragraph
            if(char == '\n'):
                char = ''
                column += self.spacing.right - 1
                newline = True
                newparagraph = True

            # Width Limit into New Line
            elif(column == self.width - self.spacing.right):
                column += self.spacing.right
                newline = True

            if(column > width):
                width = column

            # Check Limit and add New Line
            if(newline):
                newline = False

                # Height Limit
                if(line == self.height - self.spacing.bottom):
                    height += self.spacing.bottom
                    return width, height

                column = self.spacing.left + 1
                line   += 1
            
            if(line > height):
                height = line

        # Bottom Margin
        height += self.spacing.bottom

        return width, height
    
    
    #   Return the text with the formatting applied
    def __str__(self):
        string = ''

        paragraph = self.GetParagraph()
        width = self.MaxWidth() # Not checking by column == 0 makes things easier

        column = paragraph  # Number of Columns in current Line
        line   = 1          # Number of Lines in current String

        # Top Margin
        line += self.spacing.top
        for i in range(self.spacing.top):
            string += '\n'
        
        # Initial Left Spacing
        string += ' ' * self.spacing.left

        newline = False
        newparagraph = True
        for char in self.text:
            
            # Paragraph Spacing
            if(newparagraph):
                newparagraph = False
                string += ' ' * paragraph
                column = paragraph + self.spacing.left
            
            # New Line to Paragraph
            if(char == '\n'):
                char = ''
                newline = True
                newparagraph = True
            
            # Width Limit to New Line░
            elif(column == width - self.spacing.right):
                newline = True
            
            else:
                string += char
                column += 1
            
            # Check Limit and add New Line
            if(newline):
                newline = False

                # Height Limit
                if(line == self.height - self.spacing.bottom):

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
                    for i in range(self.spacing.bottom):
                        string += '\n'
                        
                    return string
                
                # Add Newline
                string += '\n' + ' ' * self.spacing.left + char
                column = self.spacing.left + 1
                line   += 1
        
        # Bottom Margin
        for i in range(self.spacing.bottom):
            string += '\n'
        
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
    test.SetParagraph(int(input('paragraph:')))
    test.SetMargin(int(input('Margin\nLeft:')), int(input('Right:')), int(input('Top:')), int(input('Bottom:')))

    for i in range(test.MaxWidth()):
        if((i+1)%10):
            print('_', end='')
        else:
            print(int((i+1)/10), end='')
    print('')
    
    for i in range(test.MaxWidth()):
        print((i+1)%10, end='')
    print('')
    
    print(str(test))
    print(test.Size())