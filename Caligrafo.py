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
    

    def SetMargin(self, amount: int):
        if(amount < 0):
            return False
        self.left = self.right = self.top = self.bottom = amount
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
    

    #   Horizontal = left; center; right; justified. Vertical = top; center; bottom.
    def SetAlignment(self, horizontal: str | None = '', vertical: str | None = ''):
        # Resets
        if(not horizontal and not vertical):
            horizontal = 'left'
            vertical = 'top'

        if(horizontal):
            horizontal = horizontal.lower()
            if(horizontal != 'left' and horizontal != 'center' and horizontal != 'right' and horizontal != 'justified'):
                return False
            self.alignH = horizontal
        
        if(vertical):
            vertical = vertical.lower()
            if(vertical != 'top' and vertical != 'center' and vertical != 'bottom'):
                return False
            self.alignV = vertical
            
        return True
    

    def SetMargin(self, amount: int):
        return self.spacing.SetMargin(amount)
    

    def SetParagraph(self, amount: int):
        return self.spacing.SetParagraph(amount)
    

    # Reduce the paragraph spacing if width is too small
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
    

    #   Return the text with the formatting applied
    def __str__(self):
        string = ''

        paragraph = self.GetParagraph()
        width = self.MaxWidth() # Not checking by column == 0 makes things easier

        column = paragraph  # Number of Columns in current Line
        line   = 1          # Number of Lines in current String

        # Top Margin
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
            
            # New Line into Paragraph
            if(char == '\n'):
                char = ''
                newline = True
                newparagraph = True
            
            # Width Limit into New Line
            elif(column == width - self.spacing.right):
                newline = True
            
            else:
                string += char
                column += 1
            
            # Check Limit and add New Line
            if(newline):
                newline = False

                # Height Limit
                if(line == self.height):

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
    test.SetMargin(3)
    
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