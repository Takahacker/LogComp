section .data
  format_out: db "%d", 10, 0
  format_in: db "%d", 0
  scan_int: dd 0

section .text
  extern printf
  extern scanf
  global _start

add:
  push ebp
  mov ebp, esp
  mov eax, [ebp+12]
  push eax
  mov eax, [ebp+8]
  pop ecx
  add eax, ecx
  mov esp, ebp
  pop ebp
  ret
  mov esp, ebp
  pop ebp
  ret
double:
  push ebp
  mov ebp, esp
  mov eax, 2
  push eax
  mov eax, [ebp+8]
  pop ecx
  imul ecx
  mov esp, ebp
  pop ebp
  ret
  mov esp, ebp
  pop ebp
  ret

_start:
  push ebp
  mov ebp, esp
  sub esp, 4
  mov eax, 4
  push eax
  mov eax, 3
  push eax
  call add
  add esp, 8
  mov [ebp-4], eax
  mov eax, [ebp-4]
  push eax
  push format_out
  call printf
  add esp, 8
  sub esp, 4
  mov eax, [ebp-4]
  push eax
  call double
  add esp, 4
  mov [ebp-8], eax
  mov eax, [ebp-8]
  push eax
  push format_out
  call printf
  add esp, 8
  mov eax, 2
  push eax
  mov eax, 1
  push eax
  call add
  add esp, 8
  push eax
  mov eax, 10
  push eax
  call add
  add esp, 8
  push eax
  push format_out
  call printf
  add esp, 8
  mov esp, ebp
  pop ebp
  mov eax, 1
  xor ebx, ebx
  int 0x80
