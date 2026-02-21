from src.funktion import Funktion,Punkt

f = Funktion("-2x^3 +15x^2 -24x +10")
hoch_punkt = f.extrem_punkte()["hoch_punkte"][0]
tief_punkt = f.extrem_punkte()["tief_punkte"][0]
wende_punkte = f.wende_punkte()
richtung_p_unendlich = f.global_verhalten()["p_unendlich"]
sekante_steigung_von_1_bis_3 = f.durchschnittliche_änderungsrate(von=1,bis=3)
null_punkte = f.null_punkte()

g = Funktion("x^4")

print(g.aufleitung())

