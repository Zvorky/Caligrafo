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
        March     2023     |||
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
    

    def CenterMargin(self):
        self.left = self.right = (self.left + self.right) / 2
        self.top = self.bottom = (self.top + self.bottom) / 2



class TextBox:
    def __init__(self, text = '', width = 0, heigth = 0):
        self.text = text
        self.width = width
        self.heigth = heigth
        self.spacing = Spacing()
        self.alignH = 'left'
        self.alignV = 'top'
    

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
    

    def CenterMargin(self):
        self.spacing.CenterMargin()
    

    #   Return the text with the formatting applied
    def ConvertStr(self):
        if(self.width > 0 and self.spacing.paragraph >= self.width):
            paragraph = (self.width-1)
        else:
            paragraph = self.spacing.paragraph
        
        string  = ' ' * paragraph
        columns = paragraph
        lines   = 1

        for letter in self.text:
            columns += 1

            string += letter

            if(letter == '\n'):         # New Line → Paragraph
                string += ' ' * paragraph
                columns = paragraph
                lines += 1

            if(self.width > 0 and columns == self.width):    # Width Limit → New Line
                string += '\n'
                columns = 0
                lines += 1
            
        return string

test = TextBox('xdddddddddddddddddd\no.o')
test.heigth = 2
test.width = 11
print(test.ConvertStr())