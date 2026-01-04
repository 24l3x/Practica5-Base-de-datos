# Practica5-Base-de-datos
## Edición de valores de una base de datos relacional empleando DML
### Ejercicios:
#### 1. ✅ 2. ✅ 3.❌ 4.❌

***Orden***
	
	practica5/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── entrypoint.sh
    ├── requirements.txt
    ├── sql/
    │   └── init.sql     
    └── scripts/
        ├── poblar_leve.py
        ├── poblar_moderado.py
        └── poblar_masivo.py


### Ejercicio 1
#### MER
![MER](https://github.com/user-attachments/assets/0998288f-59a3-4053-a1f4-c84d26f83d55)
**DDL en carpeta sql**

### Ejercicio 2
#### Capturas Ejecucion
##### Nivel 1
![Leve](https://github.com/user-attachments/assets/3dd90922-4dce-42cd-9501-4a1853754215)


##### Nivel 2
![Moderado](https://github.com/user-attachments/assets/fe9993fc-2878-4957-be36-4da08ed8a647)

##### Nivel 3
<img width="682" height="280" alt="Masivo" src="https://github.com/user-attachments/assets/645b9258-ff2f-422a-93b5-05cf1a4a0d68" />

#### Tabla Comparativa
|  Metrica | Nivel 1 | Nivel 2 | Nivel 3  |
| ------------ | ------------ | ------------ | ------------ |
| Total de registros  | 500  | 88,068  | 1,060,022  |
| Tiempo de ejecución  | 0.5s | 25.3s  | 34.23s  |
| Resgistros/segundo  | 1,000  | 3,480.95  | 30,967.64  |
| Uso de memoria (MB) | 518.43 Mb  | 414.43 Mb  | 504 Mb  |
| Tamaño de BD (MB) | 0.2 Mb  | 9.08 Mb  | 91.53 Mb  |

##### SQL para Total de registros y Tamaño de BD
###### Total de registros
```sql
SELECT 
    (SELECT COUNT(*) FROM Cliente) +
    (SELECT COUNT(*) FROM Productos) +
    (SELECT COUNT(*) FROM Pedido) +
    (SELECT COUNT(*) FROM Detalle_Pedido) +
    (SELECT COUNT(*) FROM Pagos) AS "Total Registros Insertados";
```
###### Tamaño de BD
```sql
SELECT 
    table_schema AS "Base de Datos", 
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Tamaño (MB)" 
FROM information_schema.TABLES 
WHERE table_schema = 'tienda_abarrotes';
```
