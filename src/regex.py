from typing import List,Union
from src.mather import Term,AbsolutesGlied
import re

def parseFunktion(funktion_string: str) -> List[Union[Term, AbsolutesGlied]]:
    terme: List[Union[Term, AbsolutesGlied]] = []
    
    funktion_string = funktion_string.strip()
    term_strings = re.split(r'\s+', funktion_string)
    
    for i, term_str in enumerate(term_strings):
        if not term_str:
            continue
        
        vorzeichen = "+"
        if term_str.startswith("+") or term_str.startswith("-"):
            vorzeichen = term_str[0]
            term_str = term_str[1:]
        elif i == 0:
            vorzeichen = "+"
        
        pattern = r'^(\d*)?([a-zA-Z]+)?(?:\^(\d+))?$'
        match = re.match(pattern, term_str)
        
        if not match:
            continue
        
        koeff_str, name_str, exp_str = match.groups()
        
        if name_str:
            koeffizient = int(koeff_str) if koeff_str else 1
            exponent = int(exp_str) if exp_str else 1
            terme.append(Term(
                vorzeichen=vorzeichen,
                koeffizient=koeffizient,
                name=name_str,
                exponent=exponent
            ))
        else:
            koeffizient = int(koeff_str) if koeff_str else 0
            if koeffizient != 0:
                terme.append(AbsolutesGlied(
                    value=abs(koeffizient),
                    vorzeichen=vorzeichen
                ))
    
    return terme