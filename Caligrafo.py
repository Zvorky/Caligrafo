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
        self.left = self.right = self.top = self.bottom
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
        
        max = 0
        column = 0
        for char in self.text:
            if(char == '\n'):
                column = 0
            else:
                column += 1
            
            if(column > max):
                max = column
        return max
    

    #   Return the text with the formatting applied
    def __str__(self):
        string = ''

        # Reduce the paragraph spacing if needed
        if(self.width > 0 and self.spacing.paragraph >= self.width):
            paragraph = (self.width-1)
        else:
            paragraph = self.spacing.paragraph

        column = paragraph  # Number of Columns in current Line
        line   = 1          # Number of Lines in current String

        newline = False
        newparagraph = True
        for char in self.text:
            
            # Paragraph Spacing
            if(newparagraph):
                newparagraph = False
                string += ' ' * paragraph
                column = paragraph
            
            # New Line into Paragraph
            if(char == '\n'):
                char = ''
                newline = True
                newparagraph = True
            
            # Width Limit into New Line
            elif(column == self.width):
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
                        if(self.width):
                            string += ' ' * (self.width - column)
                            string = string[0:len(string) - len(self.limitMsg)]
                    
                    if(len(self.limitMsg) > self.width and line > 1):
                        string += '\n'
                    
                    string += self.limitMsg
                    
                    return string
                
                # Add Newline
                string += '\n' + char
                column = 1
                line   += 1
            
        return string



if __name__ == '__main__':
    test = TextBox('xdddddddddddddddddd.\no.o\n.-.')
    test.Resize(int(input('width:')), int(input('height:')))
    test.SetParagraph(int(input('paragraph:')))
    
    print('_'*test.MaxWidth())
    for i in range(test.MaxWidth()):
        print((i+1)%10, end='')
    print('')
    
    print(str(test))