from typing import Union,List
from src.regex import parseFunktion
from src.mather import Term,AbsolutesGlied,Punkt,GlobalVerhalten,ExtremPunkte

class Funktion:
    def __init__(self,terme:Union[List[Union[Term, AbsolutesGlied, int]],str]):
        if isinstance(terme,str):
            self.terme = parseFunktion(terme)
        else:
            self.terme = terme


    def __call__(self,value:int) -> float:
        lösungen:List[float] = []
        for term in self.terme:
            ausrechnung = None
            if isinstance(term,Term): 
                ausrechnung = term.ausrechnen(value) 
            elif isinstance(term,AbsolutesGlied):
                ausrechnung = term.value if term.vorzeichen == "+" else -term.value
            else:
                ausrechnung = 0
            lösungen.append(ausrechnung)
        ergebnis = 0.0
        for lösung in lösungen:
            ergebnis += lösung
        return ergebnis


    def ableitung(self,wie_vielte_ableitung:int = 1) -> "Funktion":
        if wie_vielte_ableitung <= 0:
            return self
        
        result = self
        for _ in range(wie_vielte_ableitung):
            new_terme:List[Union[Term, AbsolutesGlied, int]] = []
            for term in result.terme:
                if isinstance(term, AbsolutesGlied):
                    new_terme.append(0)
                elif isinstance(term, Term):
                    if term.exponent == 0:
                        new_terme.append(0)
                    else:
                        new_koeffizient = term.koeffizient * term.exponent
                        new_exponent = term.exponent - 1
                        if new_exponent == 0:
                            new_terme.append(AbsolutesGlied(
                                value=abs(new_koeffizient),
                                vorzeichen=term.vorzeichen
                            ))
                        else:
                            new_terme.append(Term(
                                koeffizient=new_koeffizient,
                                exponent=new_exponent,
                                vorzeichen=term.vorzeichen,
                                name=term.name
                            ))
                else:
                    new_terme.append(0)
            result = Funktion(new_terme)
        return result


    def aufleitung(self,wie_vielte_aufleitung:int = 1) -> "Funktion":
        if wie_vielte_aufleitung <= 0:
            return self
        
        result = self
        for _ in range(wie_vielte_aufleitung):
            new_terme:List[Union[Term, AbsolutesGlied, int]] = []
            for term in result.terme:
                if isinstance(term, AbsolutesGlied):
                    new_terme.append(Term(
                        koeffizient=term.value,
                        exponent=1,
                        vorzeichen=term.vorzeichen,
                        name="x"
                    ))
                elif isinstance(term, Term):
                    new_exponent = term.exponent + 1
                    new_koeffizient = term.koeffizient / new_exponent
                    new_terme.append(Term(
                        koeffizient=new_koeffizient,
                        exponent=new_exponent,
                        vorzeichen=term.vorzeichen,
                        name=term.name
                    ))
                else:
                    new_terme.append(Term(
                        koeffizient=1,
                        exponent=1,
                        vorzeichen="+",
                        name="x"
                    ))
            result = Funktion(new_terme)
        return result


    def global_verhalten(self) -> GlobalVerhalten:
        alle_exponenten = [term.exponent for term in self.terme if isinstance(term,Term)]
        if not alle_exponenten:
            return {
                "p_unendlich":"f(x) -> konstant",
                "m_unendlich":"f(x) -> konstant"
            }
        höchster_exponent = max(alle_exponenten)
        grader_exponent = höchster_exponent % 2 == 0
        höchste_terme = [term for term in self.terme if isinstance(term,Term) and term.exponent == höchster_exponent]
        if not höchste_terme:
            return {
                "p_unendlich":"f(x) -> konstant",
                "m_unendlich":"f(x) -> konstant"
            }
        main_term = höchste_terme[0]
        koeffizient_positiv = main_term.koeffizient > 0 if main_term.vorzeichen == "+" else main_term.koeffizient < 0
        
        if grader_exponent and koeffizient_positiv:
            return {
                "p_unendlich":"f(x) -> +unendlich",
                "m_unendlich":"f(x) -> +unendlich"
            }
        elif grader_exponent and not koeffizient_positiv:
            return {
                "p_unendlich":"f(x) -> -unendlich",
                "m_unendlich":"f(x) -> -unendlich"
            }
        elif not grader_exponent and koeffizient_positiv:
            return {
                "p_unendlich":"f(x) -> +unendlich",
                "m_unendlich":"f(x) -> -unendlich"
            }
        else:
            return {
                "p_unendlich":"f(x) -> -unendlich",
                "m_unendlich":"f(x) -> +unendlich"
            }


    def integrieren(self,von:int,bis:int) -> float:
        F = self.aufleitung()
        return F(bis) - F(von)


    def null_punkte(self, suchbereich_start: int = -100, suchbereich_ende: int = 100, schrittweite: float = 1.0, genauigkeit: float = 0.001) -> List[Punkt]:
        nullpunkte:List[Punkt] = []
        x = float(suchbereich_start)
        
        while x < suchbereich_ende:
            y1, y2 = self(x), self(x + schrittweite)
            
            if abs(y1) < genauigkeit:
                if not any(abs(np.x - x) < genauigkeit for np in nullpunkte):
                    nullpunkte.append(Punkt(x=x, y=0))
            elif (y1 > 0 and y2 < 0) or (y1 < 0 and y2 > 0):
                a, b, y_a = x, x + schrittweite, y1
                while abs(b - a) > genauigkeit:
                    mitte = (a + b) / 2
                    y_mitte = self(mitte)
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
                bisschen_vor_is_positiv = fs(np.x - 0.1) > 0
                bisschen_nach_is_positiv = fs(np.x + 0.1) > 0
                
                if bisschen_vor_is_positiv and not bisschen_nach_is_positiv:
                    hoch_punkte.append(Punkt(x=np.x, y=self(np.x)))
                elif not bisschen_vor_is_positiv and bisschen_nach_is_positiv:
                    tief_punkte.append(Punkt(x=np.x, y=self(np.x)))
                else:
                    sattel_punkte.append(Punkt(x=np.x, y=self(np.x)))
        
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
            bisschen_vor = fss(np.x - 0.1)
            bisschen_nach = fss(np.x + 0.1)
            if abs(bisschen_vor) < 0.001 and abs(bisschen_nach) < 0.001:
                continue
            if (bisschen_vor > 0 and bisschen_nach < 0) or (bisschen_vor < 0 and bisschen_nach > 0):
                wende_punkte.append(Punkt(x=np.x, y=self(np.x)))
        return wende_punkte


    def tangente(self,stelle:int) -> "Funktion":
        tangenten_terme:List[Union[Term,AbsolutesGlied,int]] = []
        tangenten_punkt = Punkt(x=stelle,y=self(stelle))
        fs = self.ableitung()
        steigung = fs(stelle)
        
        y_achsenabschnitt = tangenten_punkt.y - steigung * tangenten_punkt.x
        
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


    def sekante(self, stelle1: float, stelle2: float) -> "Funktion":
        if stelle1 == stelle2:
            raise ValueError("Sekante braucht zwei verschiedene Stellen")
        p1 = Punkt(x=stelle1, y=self(stelle1))
        p2 = Punkt(x=stelle2, y=self(stelle2))
        steigung = (p2.y - p1.y) / (p2.x - p1.x)
        y_achsenabschnitt = p1.y - steigung * p1.x

        sekanten_terme: List[Union[Term, AbsolutesGlied, int]] = []
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


    def durchschnittliche_änderungsrate(self,von:int,bis:int) -> int:
        return (self(bis) - self(von)) / (bis - von)


    def __add__(self, other: "Funktion") -> "Funktion":
        neue_terme: List[Union[Term, AbsolutesGlied, int]] = []
        
        for term in self.terme:
            neue_terme.append(term)
        
        for term in other.terme:
            if isinstance(term, Term):
                neue_terme.append(Term(
                    koeffizient=term.koeffizient,
                    exponent=term.exponent,
                    vorzeichen=term.vorzeichen,
                    name=term.name
                ))
            elif isinstance(term, AbsolutesGlied):
                neue_terme.append(AbsolutesGlied(
                    value=term.value,
                    vorzeichen=term.vorzeichen
                ))
        
        return Funktion(neue_terme)

    def __sub__(self, other: "Funktion") -> "Funktion":
        neue_terme: List[Union[Term, AbsolutesGlied, int]] = []
        
        for term in self.terme:
            neue_terme.append(term)
        
        for term in other.terme:
            if isinstance(term, Term):
                umgekehrtes_vorzeichen = "-" if term.vorzeichen == "+" else "+"
                neue_terme.append(Term(
                    koeffizient=term.koeffizient,
                    exponent=term.exponent,
                    vorzeichen=umgekehrtes_vorzeichen,
                    name=term.name
                ))
            elif isinstance(term, AbsolutesGlied):
                umgekehrtes_vorzeichen = "-" if term.vorzeichen == "+" else "+"
                neue_terme.append(AbsolutesGlied(
                    value=term.value,
                    vorzeichen=umgekehrtes_vorzeichen
                ))
        
        return Funktion(neue_terme)

    def __str__(self) -> str:
        teile = []
    
        for i, term in enumerate(self.terme):
            if isinstance(term, int) and term == 0:
                continue
            
            if isinstance(term, Term):
                vorzeichen_str = ""
                if i == 0:
                    if term.vorzeichen == "-":
                        vorzeichen_str = "-"
                else:
                    vorzeichen_str = " " + term.vorzeichen + " "
                
                koeff_str = ""
                if term.koeffizient == 1:
                    if term.exponent == 0:
                        koeff_str = "1"
                else:
                    koeff_str = str(int(term.koeffizient))
                
                if term.exponent == 0:
                    teile.append(vorzeichen_str + koeff_str)
                elif term.exponent == 1:
                    teile.append(vorzeichen_str + (koeff_str if koeff_str != "1" else "") + term.name)
                else:
                    teile.append(vorzeichen_str + (koeff_str if koeff_str != "1" else "") + term.name + "^" + str(term.exponent))
            
            elif isinstance(term, AbsolutesGlied):
                vorzeichen_str = ""
                if i == 0:
                    if term.vorzeichen == "-":
                        vorzeichen_str = "-"
                else:
                    vorzeichen_str = " " + term.vorzeichen + " "
                
                teile.append(vorzeichen_str + str(term.value))
        
        if not teile:
            return "f(x) = 0"

        return f"y = " + "".join(teile).strip()