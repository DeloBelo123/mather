from typing import Self,List,Literal,Union,TypedDict
from pydantic import BaseModel

class AbsolutesGlied(BaseModel):
    value:int
    vorzeichen:Literal["+"|"-"]

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
    def divide(a:int,b:int) -> int:
        return a / b
    @staticmethod
    def power(a:int,b:int) -> int:
        return a ** b

class Term:
    def __init__(
        self:Self,
        vorzeichen:Literal["+" | "-"] = "+",
        koeffizient:int = 1,
        name:Union[str | AbsolutesGlied] = "x",
        exponent:int = 0
    ):
        self.koeffizient = koeffizient
        self.name = name
        self.exponent = exponent
        self.vorzeichen = vorzeichen

    def ausrechnen(self,value:int) -> int:
        exponentiert = Calc.power(value,self.exponent)
        koeffizientiert = Calc.multiply(exponentiert,self.koeffizient)
        ergebnis = koeffizientiert if self.vorzeichen == "+" else -koeffizientiert
        return ergebnis

class Funktion:

    def __init__(self,terme:List[Term | AbsolutesGlied | 0]):
        self.terme = terme


    def von(self,value:int) -> int:
        lösungen:List[int] = []
        for term in self.terme:
            ausrechnung = None
            if isinstance(term,Term): 
                ausrechnung = term.ausrechnen(value) 
            elif isinstance(term,AbsolutesGlied):
                ausrechnung = term.value
            else:
                ausrechnung = 0
            lösungen.append(ausrechnung)
        ergebnis = 0
        for lösung in lösungen:
            ergebnis += lösung
        return ergebnis


    def ableitung(self,wie_vielte_ableitung:int = 1) -> "Funktion":
        new_terme:List[Term | AbsolutesGlied | 0] = []
        for term in self.terme:
            new_koeffizient = None
            new_exponent = None
            for _ in range(wie_vielte_ableitung):
                term.koeffizient = term.exponent * term.koeffizient
                if term.exponent == 1:
                    new_terme.append(AbsolutesGlied(term.koeffizient))
                    continue
                if isinstance(term,AbsolutesGlied):
                    new_terme.append(0)
                    continue
                term.exponent = term.exponent - 1
                new_koeffizient = term.koeffizient
                new_exponent = term.exponent
            new_terme.append(Term(
                koeffizient=new_koeffizient,
                exponent=new_exponent,
                vorzeichen=term.vorzeichen,
                name=term.name
            ))
        return Funktion(new_terme)


    def aufleitung(self,wie_vielte_aufleitung:int = 1) -> "Funktion":
        new_terme:List[Term | AbsolutesGlied | 0] = []
        for term in self.terme:
            new_koeffizient = None
            new_exponent = None
            for _ in range(wie_vielte_aufleitung):
                term.exponent = term.exponent + 1
                term.koeffizient = term.koeffizient / term.exponent
                if isinstance(term, AbsolutesGlied):
                    new_term = Term(
                        koeffizient=term.value,
                        exponent=1,
                        vorzeichen=term.vorzeichen,
                        name="x"
                    )
                    new_terme.append(new_term)
                    continue
                
                if isinstance(term, int) and term == 0:
                    new_terme.append(0)
                    continue
                new_koeffizient = term.koeffizient
                new_exponent = term.exponent
            new_terme.append(Term(
                koeffizient=new_koeffizient,
                exponent=new_exponent,
                vorzeichen=term.vorzeichen,
                name=term.name
            ))
        return Funktion(new_terme)


    def global_verhalten(self) -> GlobalVerhalten:
        alle_exponenten = [term.exponent for term in self.terme if isinstance(term,Term)]
        höchster_exponent = max(alle_exponenten) 
        grader_exponent = höchster_exponent % 2 == 0
        main_vorzeichen = list(filter(lambda term:term.exponent == höchster_exponent if isinstance(term,Term) else 0,self.terme))[0].vorzeichen
        if grader_exponent and main_vorzeichen == "+":
            return {
                "p_unendlich":"f(x) -> +unendlich",
                "m_unendlich":"f(x) -> +unendlich"
            }
        elif grader_exponent and main_vorzeichen == "-":
            return {
                "p_unendlich":"f(x) -> -unendlich",
                "m_unendlich":"f(x) -> -unendlich"
            }
        elif not grader_exponent and main_vorzeichen == "+":
            return {
                "p_unendlich":"f(x) -> +unendlich",
                "m_unendlich":"f(x) -> -unendlich"
            }
        else:
            return {
                "p_unendlich":"f(x) -> -unendlich",
                "m_unendlich":"f(x) -> +unendlich"
            }


    def integrieren(self,von:int,bis:int) -> int:
        F = self.aufleitung()
        return F.von(bis) - F.von(von)


    def null_punkte(self, suchbereich_start: int = -100, suchbereich_ende: int = 100, schrittweite: float = 1.0, genauigkeit: float = 0.001) -> List[Punkt]:
        nullpunkte:List[Punkt] = []
        x = float(suchbereich_start)
        
        while x < suchbereich_ende:
            y1, y2 = self.von(x), self.von(x + schrittweite)
            
            if abs(y1) < genauigkeit:
                if not any(abs(np.x - x) < genauigkeit for np in nullpunkte):
                    nullpunkte.append(Punkt(x=x, y=0))
            elif (y1 > 0 and y2 < 0) or (y1 < 0 and y2 > 0):
                a, b, y_a = x, x + schrittweite, y1
                while abs(b - a) > genauigkeit:
                    mitte = (a + b) / 2
                    y_mitte = self.von(mitte)
                    if abs(y_mitte) < genauigkeit:
                        nullpunkt = Punkt(x=mitte, y=0)
                        break
                    if y_a * y_mitte < 0:
                        b = mitte
                    else:
                        a, y_a = mitte, y_mitte
                else:
                    nullpunkt = Punkt(x=(a + b) / 2, y=0)
                
                if not any(abs(np.x - nullpunkt.x) < genauigkeit for np in nullpunkte):
                    nullpunkte.append(nullpunkt)

            x += schrittweite 
        return nullpunkte


    def extrem_punkte(self) -> ExtremPunkte:
        fs = self.ableitung()
        null_punkte = fs.null_punkte()

        hoch_punkte: List[Punkt] = []
        tief_punkte: List[Punkt] = []
        sattel_punkte: List[Punkt] = []
        
        if len(null_punkte) > 0:
            for np in null_punkte:
                bisschen_vor_is_positiv = fs.von(np.x - 0.1) > 0
                bisschen_nach_is_positiv = fs.von(np.x + 0.1) > 0
                
                if bisschen_vor_is_positiv and not bisschen_nach_is_positiv:
                    hoch_punkte.append(Punkt(x=np.x, y=self.von(np.x)))
                elif not bisschen_vor_is_positiv and bisschen_nach_is_positiv:
                    tief_punkte.append(Punkt(x=np.x, y=self.von(np.x)))
                else:
                    sattel_punkte.append(Punkt(x=np.x, y=self.von(np.x)))
        
        return {
            "hoch_punkte": hoch_punkte,
            "tief_punkte": tief_punkte,
            "sattel_punkte": sattel_punkte
        }

    def wende_punkte(self) -> List[Punkt]:
        fss = self.ableitung().ableitung()
        null_punkte = fss.null_punkte()
        wende_punkte:List[Punkt] = []
        for np in null_punkte:
            bisschen_vor_is_positiv = fss.von(np.x - 0.1) > 0
            bisschen_nach_is_positiv = fss.von(np.x + 0.1) > 0
            if bisschen_vor_is_positiv and not bisschen_nach_is_positiv:
                wende_punkte.append(Punkt(x=np.x, y=self.von(np.x)))
        return wende_punkte

        

            





    

