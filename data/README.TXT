Primeiro:

Retirar do arquivo .log todos os átomos que se movem ao longo da simulação.
Estes átomos aparecem com o label "0" logo após a definição do tipo de ãtomo.

Segundo:

Retirar do arquivo .log somente os átomos que participam da parte "High Level" do cálculo
Estes átomos apárem com o label "H" ao término da definição das coordenadas, como mostrado 
no exemplo abaixo:

H-H_(PDBName=H4,ResName=D1N,ResNum=1637_A)          0   22.85600000   18.45700000   16.24900000 H

Os átos que também participam da fronteira QM/MM também devem ser removidos. 
Estes átomos aparecem com o label "L H" como mostrado no exemplo abaixo:

H-H_(PDBName=H7,ResName=D1N,ResNum=1637_A)          0   26.51600000   20.77400000   17.84200000 L H-H_ 4567

Este exemplo acima diz que o átomo H-H_ faz parte da fronteira e está ligado no átomo 4567


É isso aí...

Desde já te agradeço