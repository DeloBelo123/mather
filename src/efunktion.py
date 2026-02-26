import math
import re
from typing import List,Union
from src.mather import Punkt,GlobalVerhalten,ExtremPunkte


def parseEFunktion(funktions_string:str) -> tuple:
    s = funktions_string.strip()
    pattern = r'^([+-]?\d*\.?\d*)\*?e\^([+-]?\d*\.?\d*)x(?:\s*([+-]\s*\d+\.?\d*))?$'
    match = re.match(pattern, s)
    if not match:
        raise ValueError(f"Ungültiges E-Funktions-Format: {s}")

    a_str,c_str,b_str = match.groups()

    if a_str in ('','+'):
        a = 1.0
    elif a_str == '-':
        a = -1.0
    else:
        a = float(a_str)

    if c_str in ('','+'):
        c = 1.0
    elif c_str == '-':
        c = -1.0
    else:
        c = float(c_str)

    b = 0.0 if b_str is None else float(b_str.replace(' ',''))

    return a,c,b


def _zahl_str(n:float) -> str:
    if n == int(n):
        return str(int(n))
    return str(round(n,4))


class EFunktion:
    def __init__(self,eingabe:Union[str,tuple]):
        if isinstance(eingabe,str):
            self.a,self.c,self.b = parseEFunktion(eingabe)
        elif isinstance(eingabe,tuple) and len(eingabe) == 3:
            self.a,self.c,self.b = float(eingabe[0]),float(eingabe[1]),float(eingabe[2])
        else:
            raise ValueError("Eingabe muss ein String oder ein Tupel (a, c, b) sein")


    def __call__(self,x:float) -> float:
        return self.a * math.exp(self.c * x) + self.b


    def ableitung(self,wie_vielte_ableitung:int = 1) -> "EFunktion":
        if wie_vielte_ableitung <= 0:
            return self
        result = self
        for _ in range(wie_vielte_ableitung):
            result = EFunktion((result.a * result.c, result.c, 0.0))
        return result


    def aufleitung(self,wie_vielte_aufleitung:int = 1) -> "EFunktion":
        if wie_vielte_aufleitung <= 0:
            return self
        result = self
        for _ in range(wie_vielte_aufleitung):
            if result.c == 0:
                raise ValueError("Aufleitung nicht möglich wenn c = 0")
            result = EFunktion((result.a / result.c, result.c, 0.0))
        return result


    def global_verhalten(self) -> GlobalVerhalten:
        if self.c == 0:
            wert = _zahl_str(self.a + self.b)
            return {
                "p_unendlich":f"f(x) -> {wert}",
                "m_unendlich":f"f(x) -> {wert}"
            }
        b_str = _zahl_str(self.b)
        if self.c > 0:
            if self.a > 0:
                return {
                    "p_unendlich":"f(x) -> +unendlich",
                    "m_unendlich":f"f(x) -> {b_str}"
                }
            else:
                return {
                    "p_unendlich":"f(x) -> -unendlich",
                    "m_unendlich":f"f(x) -> {b_str}"
                }
        else:
            if self.a > 0:
                return {
                    "p_unendlich":f"f(x) -> {b_str}",
                    "m_unendlich":"f(x) -> +unendlich"
                }
            else:
                return {
                    "p_unendlich":f"f(x) -> {b_str}",
                    "m_unendlich":"f(x) -> -unendlich"
                }


    def integrieren(self,von:float,bis:float) -> float:
        if self.c == 0:
            return (self.a + self.b) * (bis - von)
        e_teil = (self.a / self.c) * (math.exp(self.c * bis) - math.exp(self.c * von))
        b_teil = self.b * (bis - von)
        return e_teil + b_teil


    def null_punkte(self) -> List[Punkt]:
        if self.a == 0:
            return []
        quotient = -self.b / self.a
        if quotient <= 0:
            return []
        if self.c == 0:
            return []
        x = math.log(quotient) / self.c
        return [Punkt(x=round(x,4),y=0.0)]


    def extrem_punkte(self) -> ExtremPunkte:
        return {
            "hoch_punkte":[],
            "tief_punkte":[],
            "sattel_punkte":[]
        }


    def wende_punkte(self) -> List[Punkt]:
        return []


    def tangente(self,stelle:float) -> "Funktion":
        from src.funktion import Funktion
        from src.mather import Term,AbsolutesGlied

        y_wert = self(stelle)
        steigung = self.ableitung()(stelle)
        y_achsenabschnitt = y_wert - steigung * stelle

        tangenten_terme:List[Union[Term,AbsolutesGlied,int]] = []
        tangenten_terme.append(Term(
            koeffizient=abs(steigung),
            exponent=1,
            vorzeichen="+" if steigung >= 0 else "-",
            name="x"
        ))
        if abs(y_achsenabschnitt) > 0.0001:
            tangenten_terme.append(AbsolutesGlied(
                value=abs(int(y_achsenabschnitt)),
                vorzeichen="+" if y_achsenabschnitt >= 0 else "-"
            ))
        return Funktion(tangenten_terme)


    def sekante(self,stelle1:float,stelle2:float) -> "Funktion":
        from src.funktion import Funktion
        from src.mather import Term,AbsolutesGlied

        if stelle1 == stelle2:
            raise ValueError("Sekante braucht zwei verschiedene Stellen")
        y1,y2 = self(stelle1),self(stelle2)
        steigung = (y2 - y1) / (stelle2 - stelle1)
        y_achsenabschnitt = y1 - steigung * stelle1

        sekanten_terme:List[Union[Term,AbsolutesGlied,int]] = []
        sekanten_terme.append(Term(
            koeffizient=abs(steigung),
            exponent=1,
            vorzeichen="+" if steigung >= 0 else "-",
            name="x"
        ))
        if abs(y_achsenabschnitt) > 0.0001:
            sekanten_terme.append(AbsolutesGlied(
                value=abs(int(y_achsenabschnitt)),
                vorzeichen="+" if y_achsenabschnitt >= 0 else "-"
            ))
        return Funktion(sekanten_terme)


    def durchschnittliche_änderungsrate(self,von:float,bis:float) -> float:
        return (self(bis) - self(von)) / (bis - von)


    def __add__(self,other:"EFunktion") -> "EFunktion":
        if self.c != other.c:
            raise ValueError("Addition nur möglich wenn beide den gleichen Exponenten c haben")
        return EFunktion((self.a + other.a, self.c, self.b + other.b))


    def __sub__(self,other:"EFunktion") -> "EFunktion":
        if self.c != other.c:
            raise ValueError("Subtraktion nur möglich wenn beide den gleichen Exponenten c haben")
        return EFunktion((self.a - other.a, self.c, self.b - other.b))


    def __str__(self) -> str:
        teile = []

        if self.a != 0:
            if self.a == 1:
                a_teil = ""
            elif self.a == -1:
                a_teil = "-"
            else:
                a_teil = _zahl_str(self.a) + "*"

            if self.c == 1:
                c_teil = "x"
            elif self.c == -1:
                c_teil = "-x"
            else:
                c_teil = _zahl_str(self.c) + "x"

            teile.append(f"{a_teil}e^{c_teil}")

        if self.b != 0:
            if teile:
                vz = " + " if self.b > 0 else " - "
                teile.append(f"{vz}{_zahl_str(abs(self.b))}")
            else:
                teile.append(_zahl_str(self.b))

        if not teile:
            return "y = 0"

        return "y = " + "".join(teile)
