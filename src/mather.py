from typing import Self,List,Literal,Union,TypedDict
from pydantic import BaseModel

class AbsolutesGlied(BaseModel):
    value:int
    vorzeichen:Literal["+", "-"]

class Punkt(BaseModel):
    x:float
    y:float

class GlobalVerhalten(TypedDict):
    p_unendlich:str
    m_unendlich:str

class ExtremPunkte(TypedDict):
    hoch_punkte:List[Punkt]
    tief_punkte:List[Punkt]
    sattel_punkte:List[Punkt]

class Calc:
    @staticmethod
    def add(a:int,b:int) -> int:
        return a + b
    @staticmethod
    def sub(a:int,b:int) -> int:
        return a - b
    @staticmethod
    def multiply(a:int,b:int) -> int:
        return a * b
    @staticmethod
    def divide(a:int,b:int) -> float:
        return a / b
    @staticmethod
    def power(a:int,b:int) -> float:
        return a ** b

class Term:
    def __init__(
        self:Self,
        vorzeichen:Literal["+", "-"] = "+",
        koeffizient:int = 1,
        name:Union[str | AbsolutesGlied] = "x",
        exponent:int = 0
    ):
        self.koeffizient = koeffizient
        self.name = name
        self.exponent = exponent
        self.vorzeichen = vorzeichen

    def ausrechnen(self,value:int) -> float:
        exponentiert = Calc.power(value,self.exponent)
        koeffizientiert = exponentiert * self.koeffizient
        ergebnis = koeffizientiert if self.vorzeichen == "+" else -koeffizientiert
        return ergebnis



        

            





    

