import random

def printArt():
	r1 = """\

		  CCC
		 C
		 C    ooo ooo ppp  eee rrr
		 C    o o o o p  p e e r
		  CCC ooo ooo ppp  ee r
					  p
					  p          _
								 |
		o   o                  ^ |
					  /^^^^^7  L_/
		'  '     ,oO))))))))Oo,
			   ,'))))))))))))))), /{
		  '  ,'o  ))))))))))))))))={
			 >    ))))))))))))))))={
			 `,   ))))))\ \)))))))={
			   ',))))))))\/)))))' \{
				 '*O))))))))O*'

"""

	r2 = """
COOPER!!
"""

	art = [r1,r2]
	print (random.choice(art))
