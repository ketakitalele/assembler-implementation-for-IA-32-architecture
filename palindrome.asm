section .data
	string db "madam",0
	msg db "string is palindrome",10,0
	msg1 db "string is not palindrome",10,0
section .bss
	strrev resd 1
section .text
	global main
	extern printf
main:
	mov cl,dl
	mov eax,string 
	mov ecx,dword[eax]
 	mov eax,ebx
tst:	
	mov bx,dx
	add eax,edx 
	mov ebx,ecx
	mov ecx,ebx
lp:	
	add esp,4
err:
	add esp,4
