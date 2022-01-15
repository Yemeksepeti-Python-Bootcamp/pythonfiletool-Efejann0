import csv

def openfile(adres,param=0): #dosyaları açmak için kullanılan fonsiyon
    from os import path # dosya varsa olanı açıp üstüne yazıyor
    mod = ""
    if path.exists(adres):
        mod = "a+" if param == 1 else "r+"
    else: # dosya yoksa oluşturup açıyor
        mod = "w+"
    return open(adres,mod)

def convert_list(string): #listeyi stringe çevirmek için kullanılan fonksiyon
    li = list(string.split(","))
    return li

class File_Opr:
  def __init__(self, path,fields, *args, **kwargs): #classın consturactor tanımı 
    self.path = path
    self.fields  = fields 

  def printpath(self): #hangi pathte çalıştığımızı gösteren fonksiyon
    print(self.path)

  def onelinedata(self): #sadece bir linedaki datayı değiştimeye yarayan fonksiyon
    liste=[]
    myfile = openfile(self.path)
    for i,item in enumerate(myfile.readlines()):
        liste.append(item)
        print(f"{i}:{item.split(',')}")
        if i % 5 == 0 and i != 0: #aradığımız veriyi belli çerçevelerde bize gösteriyor
          opt=input("Aradığınız veri burda mı? (Yes/No)") #bulduğuğmuzda loopu kesiyor
          if opt == "Yes" or opt == "yes":
            break
    line = int(input("lütfen line'ı girin: "))
    shape =input("seçtiğiniz satırın json olmasını istiyorsanız 1'e, variable'a aktarılmasını istiyorsanız 2'ye basın: ")
    if shape == "1": #seçilen satırın json olması isteniyorsa bu kısım devreye giriyor
      jsondata = {}
      one_linedata = list(liste[line].split(','))
      for i in range(len(self.fields)):
        jsondata[self.fields[i]] = one_linedata[i]
      import json
      with open('json.txt', 'w') as json_file:
        json.dump(jsondata, json_file)
    elif shape == "2": #bir değişkene aktarılması isteniyorsa bu kısım devreye giriyor ve return ediyor
      datadict = {}
      one_linedata = list(liste[line].split(','))
      for i in range(len(self.fields)):
        datadict[self.fields[i]] = one_linedata[i]
      return datadict

  def mergefile(self): # iki dosyayı birleştirmek için burayı kullanıyoruz 
    data2 = "" 
    liste=[]   
    merge_path = input("Please enter merge file path: ") #birleştirilicek diğer doayanın pathi alınıypr
    # Reading data from second file 
    data2 = openfile(merge_path)  
    for satir in data2: #ikinci dosya array'e çevrilip kayıt ediliyor
      liste.append(satir)
    dosya = open(self.path,"a+") # oluşturulan array ana dosyamıza ekleniyor
    for row in range(len(liste)):
      dosya.write(liste[row])
    dosya.close()

  def menu(self): #istenilen toplu işşlemlerin yapıldığı fonksiyon
      flag = True
      while flag: # yapıla bilecek işlemlerin listesi
            print("Select the action number you want to do, type exit if you want to 'exit'")
            print("1- Search")
            print("2- Delete")
            print("3- Add")
            print("4- Update")
            opt=input("The action you choose: ")

            if opt == "exit" or opt ==  "Exit":
              flag = False

            elif opt == "1": #içinde bulunan datayı arama fonksiyonu
              word = input("Enter the word you want to search: ") #istenilen kelime giriliyor
              text = csv.reader(open(self.path, "r"), delimiter=",")
              for row in text: #eğer aranan dosyada varsa olduğu satırlar bastırlıyor
                  if word in str(row):
                      print(row)

            elif opt == "2": #silinmesini istediğimiz verilerin fonsiyonu
                lines = list()
                memberName = input("Please enter a member's name to be deleted.") #bütün file arraya çeviriliyor daha sonra 
                with open(self.path, 'r') as readFile: #silinmek istenen veri bulunup arayden çıkartılıyor 
                    reader = csv.reader(readFile) #datanın olmadığı array yeniden dosyaya dönüşüyor ve kayıt ediliyor
                    for row in reader:
                        lines.append(row)
                        for field in row:
                            if field == memberName:
                                lines.remove(row)

                    with open(self.path, 'w') as writeFile:
                        writer = csv.writer(writeFile)
                        writer.writerows(lines)  

            elif opt == "3": # dosyaya yeni satır ekleme komutu
              from csv import writer
              __list=[]
              for i in range(len(self.fields)):
                  data = input( f"{self.fields[i]}: ")
                  __list.append(data)
              with open(self.path, 'a') as file_add: 
                writer_object = writer(file_add)     # Pass this file object to csv.writer() and get a writer object        
                writer_object.writerow(__list)  # Pass the list as an argument into the writerow()          
                file_add.close() # Close the file object

            elif opt == "4": #dosyada istenilen bir verinin tutulduğu yeri bulup değiştirilmesi
              liste=[]
              myfile = openfile(self.path)
              for satir in myfile:
                liste.append(satir)
              for i,item in enumerate(liste):
                print(f"{i}:{item.split(',')}")
                if i % 5 == 0 and i != 0: #belirli bir çerçevede data aratılıyor bulunca loop kesiliyor
                  opt=input("Aradığınız veri burda mı? (Yes/No)")
                  if opt == "Yes" or opt == "yes":
                    break
              line = int(input("lütfen line'ı girin: ")) # bulunan veri arraye çevirliyor ve neresinin değişmesi istediği soruluyor
              change_data =liste[line]
              change_data= convert_list(change_data) 
              for i,item in enumerate(change_data):
                print(f"{i}:{item}")
              num_chng_data =int(input("Enter the number of data you want to change: "))
              user_chng_data = input("Please enter new data: ")
              change_data[num_chng_data] = user_chng_data #istenilen değişiklik yapılınca dönüşümde oluşan karakterler siliniyor
              liste[line] = (str(change_data).replace('[','').replace(']','').replace("'","").replace("\n","")) + "\n"
              dosya = open(self.path,"w")
              for row in range(len(liste)):
                dosya.write(liste[row]) #ardından yeniden dosyaya kayır ediliyor
              dosya.close()


            else:
              print("Please select a valid action")

if __name__ == "__main__":
    fields=[]
    path = input("please enter file absolute path: ")
    choose = input("Is the fields information in the file? Yes/No : ")
    if choose == "Yes" or choose == "yes": #eğer dosyada fields bilgisi varsa onu kullanıyor yoksa kendisi oluşturuyor
       with open(path) as textfile:
           csvReader = csv.reader(textfile,delimiter=",")
           fields = list(csvReader)[0]
    else: #olmaması durumunda burası çalışıyor
        with open(path) as textfile:
           csvReader = csv.reader(textfile,delimiter=",")
           num = list(csvReader)[0]        
        for i in range(len(num)):
            fields.append(i)
    path_1 = File_Opr(path,fields)
    # path_1.printpath()
    # path_1.menu()
    # path_1.onelinedata()
    # path_1.mergefile()