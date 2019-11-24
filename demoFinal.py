import numpy as np 
import glob
import io


def readData():
	questions = []
	answers = []
	labels = []
	with open("./Data/answers.txt",'r',encoding="utf-8") as fi:	
		for line in fi:
			if line.strip() != '':
				answers.append(line.strip("\n").upper())
				
	with open("./Data/questions.txt",'r',encoding="utf-8") as fi:	
		for line in fi:
			if line.strip() != '':
				questions.append(line.strip("\n").strip('?').upper())

	with open("./Data/label_questions.txt",'r',encoding="utf-8") as fi:	
		for line in fi:
			if line.strip() != '':
				labels.append(line.strip("\n").upper())

	return questions, answers, labels

def getwords(line):
	words = line.split()
	wordl = []
	for i in range(len(words)):
		if words[i] != '?':			
			wordl.append(words[i])
	return wordl

def main():
	# Đọc File Data
	questions,answers,labels = readData() 	

	questionl = []
	answerl = []


	# Phâm nhỏ từng dòng thành từng chữ 
	for i in range(len(questions)):
		words = getwords(questions[i])
		questionl.append(words)
		answerl.append(getwords(answers[i]))

	# Lấy mảng label không bị trùng  
	label_dict = []	
	for i in range(len(labels)):
		if labels[i] not in label_dict:
			label_dict.append(labels[i])


	# Tạo từ điển cho bảng Questions kèm số lần suất hiện của chữ đó    
	word_dict = {}
	for ques in questionl:
		for word in ques:
			if word not in word_dict.keys():
				word_dict[word] = 1
			else:
				word_dict[word]+=1			


	'''
	Tạo từ điển từng chữ xuất hiện trong từng Labels kèm số 
	lần suất hiện của chữ trong từng label 	
	'''		
	word_label_dict = {}
	for i in range(len(labels)):
		for word in questionl[i]:
			if(word,labels[i]) not in word_label_dict.keys():
				word_label_dict[(word,labels[i])]=1
			else:
				word_label_dict[(word,labels[i])]+=1

			

# ----------------Phan Loại bằng Naive Bayes 
	

	# Tinh P xuat hien cua moi class so voi toan bo Data
	Pclass = {}
	for label in label_dict:
		total_thisLabel = labels.count(label) 
		Pclass[label] = total_thisLabel / len(labels)

	
	# Tinh tong so lan xuat hien cua tat ca ca chu o moi class 
	Nclass = {}
	for label in label_dict:
		count = 0
		for x in word_label_dict.keys():
			if x[1] == label:
				count+=word_label_dict[x]
		Nclass[label] = count			
	

	# Multinomial Naive Bayes voi a = 1
	d = len(word_dict)
	P_feature_class = {}
	for label in label_dict:
		for word in word_dict:
			if (word,label) in word_label_dict.keys():
				P_feature_class[(word,label)] = (word_label_dict[(word,label)]+1)/(d+Nclass[label])
			else: 
				P_feature_class[(word,label)] = 1/(d+Nclass[label])		
	

	# Nhap cau hoi 
	Input = input("Enter your question: ")	
	Input = getwords(Input.upper().strip("\n").strip('?'))
	Cmax =  [0,""]


	# Tính xác xuất cho input trong từng label và chọn ra label có xác xuất cao nhất 
	for label in label_dict:
		print("\n\n--------------------------------",label,"-------------------------")		
		result = Pclass[label]
		print("P_thisClass: ",Pclass[label])
		for word in Input:
			if (word,label) in P_feature_class.keys():
				result*= P_feature_class[(word,label)]
				print("Word:",word,"   ",P_feature_class[(word,label)])
				if (word,label) not in word_label_dict.keys():
					print("count: ",0)
				else:
					print("count: ",word_label_dict[(word,label)])
			else:
				result*=1
		print("\nP_Input of this class: ",result)
		if result > Cmax[0]:
			Cmax = [result,label]
		print("Cmax of this loop:  ",Cmax)
	print(" \n \nRESULT LABEL : ",Cmax)		
	


# ----------------Tìm câu trả lời cho Input


	# Lay cac cau hoi thuoc label Cmax
	questions_list = []
	answers_list = []
	for i in range(len(labels)):
		if labels[i] == Cmax[1]:
			questions_list.append(questionl[i])
			answers_list.append(answerl[i])


	# Chuyển các câu hỏi trong label Cmax sang dạng số theo word_dict
	question_int =[]
	for line in questions_list:
		question_int_element = []
		for word in word_dict.keys():
			count = 0
			count = line.count(word)
			question_int_element.append(count)
		question_int.append(question_int_element)

	
	# Chuyển Input sang dạng số theo word_dict
	Input_int = []
	for word in word_dict.keys():
		count = 0
		count = Input.count(word)
		Input_int.append(count)


	# Tìm câu hỏi gần đúng nhất
	VarResult = 999999  
	index = 0
	for i in range(len(question_int)):
		count = 0
		for j in  range(len(question_int[i])):
			count+= abs(question_int[i][j] - Input_int[j])

		if count < VarResult:
			index = i
			VarResult = count

	print("\n \nANSWER IS : "," ".join(answers_list[index]))




if __name__ == "__main__":
	main()

