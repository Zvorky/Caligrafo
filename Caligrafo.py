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
    def __init__(self, paragraph = 4, left = 0, right = 0, top = 0, bottom = 0):
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
    def __init__(self, text = '', width = 0, height = 0, limitTxt = '[...]'):
        self.text = text
        self.width = width
        self.height = height
        self.spacing = Spacing()
        self.alignH = 'left'
        self.alignV = 'top'
        self.limitTxt = limitTxt
    

    #   Horizontal Alignment = left; center; right; justified
    def SetAlignmentH(self, align: str):
        align = align.lower()
        if(align != 'left' and align != 'center' and align != 'right' and align != 'justified'):
            return False
        self.alignH = align
        return True
    

    #   Vertical Alignment = top; center; bottom
    def SetAlignmentV(self, align: str):
        align = align.lower()
        if(align != 'top' and align != 'center' and align != 'bottom'):
            return False
        self.alignV = align
        return True
    

    def SetMargin(self, amount: int):
        return self.spacing.SetMargin(amount)
    

    def SetParagraph(self, amount: int):
        return self.spacing.SetParagraph(amount)
    

    def CenterMargin(self):
        self.spacing.CenterMargin()
    

    #   Return the text with the formatting applied
    def ConvertStr(self):
        string = ''

        # get the right paragraph spacing
        if(self.width > 0 and self.spacing.paragraph >= self.width):
            paragraph = (self.width-1)
        else:
            paragraph = self.spacing.paragraph

        column = paragraph  # Number of Columns in current Line
        line   = 1          # Number of Lines in current String

        newparagraph = True
        for char in self.text:
            
            # Paragraph Spacing
            if(newparagraph):
                newparagraph = False
                string += ' ' * paragraph
                column = paragraph
            
            if(char == '\n'):
                # Height Limit
                if(line == self.height):
                    string += ' ' * (self.width - column)
                    if(self.width):
                        string = string[0:len(string)-len(self.limitTxt)]
                    string += self.limitTxt                        
                    return string

                # New Line into Paragraph
                newparagraph = True
                line   += 1
            
            if(column == self.width):
                string += '\n' + char
                line   += 1
                column  = 1
            
            else:
                string += char
                column += 1
            
        return string



if __name__ == '__main__':
    test = TextBox('xdddddddddddddddddd\no.o\n.-.')
    test.width = int(input('width:'))
    test.height = int(input('height:'))
    print(test.ConvertStr())