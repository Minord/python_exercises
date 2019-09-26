import pdb

def zero_to_nine(num):
	if(num >= 0 and num <= 9):
		if(num == 0):
			return 'cero'
		elif(num == 1):
			return 'uno'
		elif(num == 2):
			return 'dos'
		elif(num == 3):
			return 'tres'
		elif(num == 4):
			return 'cuatro'
		elif(num == 5):
			return 'cinco'
		elif(num == 6):
			return 'seis'
		elif(num == 7):
			return 'siete'
		elif(num == 8):
			return 'ocho'
		elif(num == 9):
			return 'nueve'
	return None

def decenas(num):
	if(num >= 1 and num <= 9):

		if(num == 1):
			return 'diez'
		elif(num == 2):
			return 'veinte'
		elif(num == 3):
			return 'treinta'
		elif(num == 4):
			return 'cuarenta'
		elif(num == 5):
			return 'cincuenta'
		elif(num == 6):
			return 'sesenta'
		elif(num == 7):
			return 'setenta'
		elif(num == 8):
			return 'ochenta'
		elif(num == 9):
			return 'noventa'
	return None

def diez2diecinueve(num):
	if(num >= 10 and num <= 19):
		if(num == 10):
			return 'diez'
		elif(num == 11):
			return 'once'
		elif(num == 12):
			return 'doce'
		elif(num == 13):
			return 'trece'
		elif(num == 14):
			return 'catorce'
		elif(num == 15):
			return 'quince'
		elif(num == 16):
			return 'dieciseis'
		elif(num == 17):
			return 'diecisiete'
		elif(num == 18):
			return 'dieciocho'
		elif(num == 19):
			return 'diecinueve'
	return None

def cero_to_19(num):
	if num < 10:
		return zero_to_nine(num)
	else:
		return diez2diecinueve(num)	

def veinte_to_99(num):
	num_str = str(num)
	firts_digit, sencond_digit = int(num_str[0]), int(num_str[1])
	if sencond_digit != 0:
		return '{} y {}'.format(decenas(firts_digit), zero_to_nine(sencond_digit))
	else: 
		return decenas(firts_digit)

def cero_to_99(num):
	if num >= 0 and num < 20:
		return cero_to_19(num)
	elif num >= 20 and num < 100:
		return veinte_to_99(num)
	return None

def cero_to_999(num):
	if num > 0 and num < 100:
		return cero_to_99(num)
	elif num == 100:
		return 'cien'
	elif num < 1000:
		num_str = str(num)
		firts_digit = int(num_str[0])
		second_digit = int(num_str[1:])

		if firts_digit == 1:
			firts_digit = 'ciento'
		elif firts_digit == 5:
			firts_digit = 'quinientos'
		elif firts_digit == 9:
			firts_digit = 'novecientos'
		else:
			firts_digit = '{}cientos'.format(zero_to_nine(firts_digit)) 

		if second_digit != 0:
			second_digit = cero_to_99(second_digit)
		else:
			second_digit = ''


		return '{} {}'.format(firts_digit, second_digit)
	return None

def cero_to_999999(num):
	if(num < 1000):
		return cero_to_999(num)
	elif(num < 1000000):
		num_str = str(num)
		size = len(num_str)
		first_len = size - 3

		firts_digit = num_str[0 : first_len]
		second_digit = num_str[first_len: first_len + 3]

		firts_digit = int(firts_digit)
		second_digit = int(second_digit)

		if firts_digit == 1:
			firts_digit = 'mil'
		else:
			firts_digit = '{} mil'.format(cero_to_999(firts_digit))

		if second_digit != 0:
			second_digit = cero_to_999(second_digit)
		else:
			second_digit = ''

		return '{} {}'.format(firts_digit, second_digit)
		
	return None

def cero_to_999999999(num):
	if(num < 1000000):
		return cero_to_999999(num)
	elif num < 1000000000:
		#dividir numeros
		num_str = str(num)
		size = len(num_str)
		first_len = size - 6

		firts_digit = num_str[0 : first_len]
		second_digit = num_str[first_len: first_len + 6]

		firts_digit = int(firts_digit)
		second_digit = int(second_digit)
		#validar y dar sentido por partes

		if firts_digit == 1:
			firts_digit = 'un millon'
		else:
			firts_digit = '{} millones'.format(cero_to_999999(firts_digit))

		if second_digit != 0:
			second_digit = cero_to_999999(second_digit)
		else:
			second_digit = ''

		return '{} {}'.format(firts_digit, second_digit)


	return None
	

def int2text(num):
	num_str = str(num)
	digit_len = len(num_str)
	
	if(digit_len <= 9):
		return cero_to_999999999(num)
	return str(num)


def main():

	while True:
		num = input('introdusca un numero: ')

		if(num == 'q'):
			break

		num = int(num)

		text_num = int2text(num)

		print('en texto el numero {} se escribe como: {}'.format(num, text_num))


if __name__ == '__main__':
	main()