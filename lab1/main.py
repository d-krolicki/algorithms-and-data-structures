import copy

from typing import Tuple, List

class Matrix:

    def __init__(self, other, initialValue:float = 0):
        self.initialValue = initialValue
        if initialValue:
            self.initialValue = initialValue
        if isinstance(other, List):
            self.__content = other
            self.rows = len(other)   #do określenia rozmiaru można użyć dowolnego z wierszy
            self.cols = len(other[0])
            self.size_:Tuple[int, int] = (self.rows, self.cols)
        if isinstance(other, Tuple):
            self.size_ = (other[0], other[1])
            self.rows = self.size_[0]
            self.cols = self.size_[1]
            result = []
            for i in range(self.rows):
                temp = []
                for j in range(self.cols):
                    temp.append(self.initialValue)
                result.append(temp)
            self.__content = result

    def __str__(self):
        cont = copy.deepcopy(self.__content)
        max_num = ""
        conv = []
        for it in cont:
            temp = [str(el) for el in it]
            conv.append(temp)
            temp = []
        for it in conv:
            for el in it:
                if len(el) > len(max_num):
                    max_num = el
        l = len(max_num)
        ct = ""
        for it in cont:
            ct += "["
            for el in it:
                ct += str(el)+((l-len(str(el))+1)*' ')
            ct = ct.rstrip()
            ct += ']\n'
        return ct


    def __add__(self, other):
        if self.size() == other.size():
            result = []
            for i in range(self.rows):
                temp = []
                row1 = self.__content[i]
                row2 = other.__content[i]
                for j in range(self.cols):
                    temp.append(row1[j] + row2[j])
                result.append(temp)
            return Matrix(result)
        else:
            raise ValueError("Matrix dimensions do not match.")

    def __getitem__(self, row):
        return self.__content[row]

    def __mul__(self, other):
        if self.cols == other.rows:
            result = Matrix((self.rows, other.cols))
            for h in range(self.rows):
                current_row = self.__content[h]   #aktualny wiersz pierwszej macierzy wykorzystywany do mnożeń
                for i in range(other.cols):
                    temp = 0
                    for j in range(len(current_row)):
                        temp += self.__content[h][j] * other.__content[j][i]
                    result[h][i] = temp
            return result
        else:
            raise ValueError("Matrix dimensions do not match.")
    
    def size(self):
        return(self.rows, self.cols)
    
def transpose(a:Matrix):
    mtx = Matrix((a.cols, a.rows), 0)
    for i in range(a.rows):
        for j in range(a.cols):
            mtx[j][i] = a[i][j]
    return mtx

def main():
    mat1 = Matrix([
        [1,0,2],
        [-1,3,1]
    ])

    mat2 = Matrix((2,3),1)

    mat3 = Matrix([
        [3,1],
        [2,1],
        [1,0]
    ])

    print("""Transpozycja macierzy\n{0}to\n{1}\nSuma macierzy\n{2}\ni\n{3}\n to\n{4}\n
    Iloczyn macierzy\n{5}\ni\n{6}\nto\n{7}""".format(mat1, transpose(mat1), mat1, mat2, mat1+mat2,
    mat1, mat3, mat1*mat3))
    return

main()
