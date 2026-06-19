# TPI - Alta de Proveedores

**Materia:** Organizacion Empresarial  
**Alumno:** Kenneth Lindner — Comisión C18   

## Descripcion

Simulador de chatbot por consola que automatiza el proceso de Alta de Proveedores para la empresa ficticia KenTech S.R.L. El sistema guía al usuario en el registro de un nuevo proveedor, validando datos, verificando duplicados y aplicando reglas de aprobación según condición fiscal.

## Requisitos

- Python 3.6 o superior

No requiere librerías externas ni conexión a internet.

## Ejecucion

```bash
python3 chatbot_alta_proveedores.py
```

## Comandos

| Comando | Función |
|---------|---------|
| `/alta` | Iniciar alta de un proveedor |
| `/listar` | Ver proveedores registrados |
| `/cancelar` | Abortar proceso en curso |
| `/salir` | Cerrar el sistema |

## Estructura del repositorio

```
├── chatbot_alta_proveedores.py   # Simulador del chatbot
├── proveedores.csv               # Base de datos (se genera automáticamente)
├── alta_proveedores_as_is.bpmn   # Diagrama BPMN - proceso actual
├── alta_proveedores_to_be.bpmn   # Diagrama BPMN - proceso automatizado
└── README.md
```

## Diagramas BPMN

Los archivos `.bpmn` se pueden visualizar en [https://demo.bpmn.io](https://demo.bpmn.io) → "Open from file".

## Proceso modelado

El bot implementa 3 compuertas exclusivas (XOR):

1. **¿CUIT válido?** — Valida formato XX-XXXXXXXX-X
2. **¿Proveedor ya registrado?** — Consulta en la BD por CUIT duplicado
3. **¿Condición fiscal?** — Responsable Inscripto (aprobación automática) vs. Monotributista/Exento (requiere aprobación del Jefe)
