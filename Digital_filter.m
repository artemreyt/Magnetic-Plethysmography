clc % очистить экран
clear all % очистить все переменные в пам€ти - в Workspace'е

koef_nomb_max = 5;
DELIMITER = ' ';
HEADERLINES = 0;
koef_nomb=5;
MU = zeros(2000);
MI = zeros(2000);
MU2 = zeros(2000);
MI2 = zeros(2000);
MU3 = zeros(2000,200);
MI3 = zeros(2000,200);
MdU = zeros(2000);


x1 = zeros((koef_nomb_max+4));
x2 = zeros((koef_nomb_max+4));
x3 = zeros(320,(koef_nomb_max+4));
 na=0;
 Aa=1300;
Bb=730;
Bbd=530;





for ind1 = 0:99
     n = num2str(ind1);
      if ind1<10
         n = ['000', n]; %#ok<AGROW>
     elseif (ind1<100)
        n = ['00', n]; %#ok<AGROW>
      end
      
      %fname =['C:\Users\vika-\Magnetic-Plethysmography\Vikameasurments','.txt'];
      fname = 'C:\Users\A564\Desktop\Magnetic-Plethysmography\Fri May  7 21-50-50 2021\1.txt';
      rawData1 = importdata(fname, DELIMITER, HEADERLINES);
      Data_I = rawData1(:,1);
      Data_U = rawData1(:,2);
      clear rawData1;
      
        for i = 1:Aa
            if  ((Data_U(i)> 10^7) || (Data_U(i)< -10^7)   )
            Data_U(i) =0;
            end   
            if  ((Data_I(i)> 10^7) || (Data_I(i)< -10^7)   )
                Data_I(i) =0;
            end  
        end
        
        for i = 1:Aa
            MI2(i) = (Data_I(i));
            MU2(i) = -(Data_U(i));
            MU(i) = 0;
            MI(i) = 0;
        end  
 
      
        
U11= MU2(3); U12=MU2(3); U10=MU2(3);
U21=MU2(3); U22=MU2(3); U20=MU2(3);
U31=MU2(3); U32=MU2(3); U30=MU2(3);
U41=MU2(3); U42=MU2(3); U40=MU2(3);

I11=MI2(3); I12=MI2(3); I10=MI2(3); 
I21=MI2(3);I22=MI2(3);I20=MI2(3);
I31=MI2(3);I32=MI2(3);I30=MI2(3);
I41=MI2(3);I42=MI2(3);I40=MI2(3);

for i = 4:Aa    
    U12=U11;      U11=U10;    
    U10 = ((MU2(i)*14347) - (MU2(i-1)*28323) + (MU2(i-2)*14347) +  ( U11*64160)-( U12*31763) )/ 32768;   
    U22=U21;     U21=U20;         
    U20 = ((U10* 11410) - (U11*22411) + (U12*11410 ) +  ( U21*61967)-( U22* 29608) )/ 32768;
    U32=U31;  U31=U30;     
    U30=( (U20* 6184) - (U21*11876) + (U22*6184 ) +  ( U31*59367)-( U32* 27090) )/ 32768;     
    U42=U41;  U41=U40;      
    U40 = ((U30* 1020) - (U31*1464) + (U32*1020  ) +  ( U41*57112)-( U42*  24919) )/ 32768;         
    MU(i)=U40;
    
    I12=I11;     I11=I10;    
    I10 = ((MI2(i)*14347) - (MI2(i-1)*28323) + (MI2(i-2)*14347) +  ( I11*64160)-( I12*31763) )/ 32768;   
    I22=I21;     I21=I20;         
    I20 = ((I10* 11410) - (I11*22411) + (I12*11410 ) +  ( I21*61967)-( I22* 29608) )/ 32768;
    I32=I31;  I31=I30;     
    I30=( (I20* 6184) - (I21*11876) + (I22*6184 ) +  ( I31*59367)-( I32* 27090) )/ 32768;     
    I42=I41;  I41=I40;      
    I40 = ((I30* 1020) - (I31*1464) + (I32*1020  ) +  ( I41*57112)-( I42*  24919) )/ 32768;         
    MI(i)=I40;
end
   

  for i = 1:Aa
            MI(i) =   (MI(i)*1.2*4.6)/(2^24*10000000);%/33554431999999.996;
            MU(i) = (MU(i)*1.2*4.6)/2^24;%/(8388608/5);
            MU1(i) =0;
            % MU1(i,ind1+1) = 0;
  end  
tmi=MI(Bb-2);
tmu= MU(Bb-2);
  for i = 1:Aa
             MI(i)=MI(i) -tmi  ;
             MU(i) = MU(i) -tmu;
  end         
  for i = 1:50
             MU(i) = 0;
  end           
  for i = Aa-50:Aa
             MU(i) = 0;
  end   

 for i = 1:Aa
     MI3(i,ind1+1) =MI(i);
     MU3(i,ind1+1) =MU(i);
 end  



end
%
        figure; hold on;
 plot(MU2); 

%       figure;
%            hold on;
%  plot(MI);
%  hold on;
%   figure;
%  plot(MU);   

   figure;
 plot(MI);
%   figure;
%  plot(MU);  
%           
%             
%             
for ind1 = 1:100  
    for i = 1:Aa
        MI(i)=MI3(i,ind1);
        MU(i)= MU3(i,ind1);
    end
    for i = 2:Aa-1
        MdU(i) = ((MU(i+1)-MU(i-1)))/(2/1953);
    end
    
    Q = zeros(2000,10);
    for cl = Bb:Bbd+Bb
        for kon = 1:koef_nomb
            Q(cl,kon) =  MU(cl)^(kon);
        end
        Q(cl,koef_nomb+1) =  MdU(cl);
    end

    A = zeros(koef_nomb+1,koef_nomb+1);
    B = zeros(1,koef_nomb+1);
    for kon1 = 1:(koef_nomb+1)
        for kon2 = 1:(koef_nomb+1)
            for cl =  Bb:Bbd+Bb
                A(kon1,kon2) = A(kon1,kon2)+(Q(cl,kon1).*Q(cl,kon2));
            end
        end
        for cl =  Bb:Bbd+Bb
            B(1, kon1) = B(1, kon1)+(MI(cl).*Q(cl,kon1));
        end
    end
        

    x(1:(koef_nomb+1)) = B/A;  
        
    for kon = 1:koef_nomb+1
        x2(kon)= x(kon);
    end 
      
    x2(koef_nomb+4)= x2(1)-3.37*10^-8;
    x2(koef_nomb+2)= 1/x2(koef_nomb+4);
    for kon = 1:koef_nomb+4
        x3(ind1,(kon))= x2(kon);
    end
%  for c2 = Bb:Bbd+Bb;
%      temp = 0;
%      for kon = 1:koef_nomb;
%          temp =  temp + x(kon)*MU1(c2)^(kon);
%      end;
%      MU1(c2+1) =(MU1(c2)+((4/1953)*(MI(c2)-temp)/(x(koef_nomb+1))+ MU1(c2-2) ))/2;
%  end;
end
%   figure;
%   hold on;
%  plot((MU1(100:1390)));%, 'LineWidth',1,'Color',[0 0 0], 'Marker','o');
   figure;
  hold on;
 plot(x3((1:100),(koef_nomb+2)));
 
 %, 'LineWidth',1,'Color',[0 0 0], 'Marker','x');
%  plot(((SADIM(5,1:9))), 'LineWidth',2,'Color',[0 0 0], 'Marker','o');


