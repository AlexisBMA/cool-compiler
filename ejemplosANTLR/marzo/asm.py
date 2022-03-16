from string import Template

tpl_start_text = """
    .text
main: 
"""

tpl_start_data = """
    .data
"""

tpl_var_decl = Template("""
$varname: .word 0
""")

tpl_end = """
    li	    $v0     10                  # 10 para terminar la emulación
    syscall
"""

tpl_immediate = Template("""
    li      $$a0    $immediate
""")

tpl_suma = Template("""
$left
    sw      $$a0    0($$sp)             # Salvar en el stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)             # Recuperar resultado parcial anterior
    addiu   $$sp    $$sp        4       # Pop
    add     $$a0    $$a0        $$t1
""")

tpl_resta = Template("""
$left
    sw      $$a0    0($$sp)             # Salvar en el stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)             # Recuperar resultado parcial anterior
    addiu   $$sp    $$sp        4       # Pop
    sub     $$a0    $$t1        $$a0
""")

tpl_print_int = Template("""
$prev
	li	    $$v0     1              # para imprimir enteros
	syscall			                # imprimir
""")

tpl_var = Template("""
    lw      $$a0        $name       # Usar variable
""")

tpl_asignacion = Template("""
$prev
    sw      $$a0        $name       # Guardar valor
""")

"""
	i: .word 0
    

	li 	$v0, 5  			# syscall to read int
	syscall					# leer int
    move	$t0,$v0         # resultado queda en $v0

    la	$t1, array	#cargar la direccion de array a $t1

.data
msg: .asciiz “\nHello, World!\n”

li $v0, 4
la $a0, msg
syscall
"""