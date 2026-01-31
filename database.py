#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
database.py
Gestión de la base de datos SQLite para RRHH Alvatross
Incluye: perfiles IT específicos, stack TM Forum/ODA, evaluación R/S/T
"""

import sqlite3
from pathlib import Path
from datetime import datetime
import csv


class DatabaseManager:
    """Clase para manejar la conexión y operaciones con SQLite"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Carpeta data en el mismo directorio que el script
            data_dir = Path(__file__).parent / "data"
            data_dir.mkdir(exist_ok=True)
            self.db_path = data_dir / "rrhh_alvatross.db"
        else:
            self.db_path = Path(db_path)
        
        self.conn = None
        self._create_tables()
    
    def connect(self):
        """Conectar a la base de datos"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    
    def disconnect(self):
        """Cerrar conexión"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
    
    def _create_tables(self):
        """Crear tablas si no existen"""
        cursor = self.connect()
        
        # ========================================
        # TABLA CANDIDATOS - Completa y específica
        # ========================================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidatos (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                email TEXT,
                telefono TEXT,
                linkedin TEXT,
                github TEXT,
                localizacion TEXT,
                remoto TEXT,
                disponibilidad TEXT,
                carnet_conducir BOOLEAN DEFAULT 0,
                vehiculo_propio BOOLEAN DEFAULT 0,
                
                -- Formación
                nivel_estudios TEXT,
                titulacion TEXT,
                certificaciones TEXT,
                idiomas TEXT,
                
                -- Experiencia profesional
                experiencia_total INTEGER DEFAULT 0,
                experiencia_telecom INTEGER DEFAULT 0,
                experiencia_tmforum TEXT,
                ultimo_puesto TEXT,
                ultima_empresa TEXT,
                proyectos TEXT,
                
                -- Stack técnico específico Alvatross
                stack_lenguajes TEXT,
                stack_frameworks TEXT,
                stack_bbdd TEXT,
                stack_cloud TEXT,
                stack_devops TEXT,
                stack_apis TEXT,
                stack_mensajeria TEXT,
                
                -- Competencias blandas
                competencias TEXT,
                
                -- RRHH y preferencias
                salario_esperado TEXT,
                estado TEXT DEFAULT 'activo',
                perfil_it TEXT,
                seniority TEXT,
                
                -- GDPR y metadata
                gdpr_consent BOOLEAN DEFAULT 0,
                fecha_registro TEXT,
                origen TEXT DEFAULT 'manual',
                notas TEXT
            )
        ''')
        
        # ========================================
        # TABLA VACANTES - Gestión de posiciones
        # ========================================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacantes (
                id TEXT PRIMARY KEY,
                titulo TEXT NOT NULL,
                perfil_it TEXT NOT NULL,
                seniority TEXT NOT NULL,
                departamento TEXT,
                ubicacion TEXT,
                modalidad TEXT,
                
                -- Requisitos técnicos
                stack_obligatorio TEXT NOT NULL,
                stack_deseable TEXT,
                experiencia_tmforum TEXT,
                experiencia_telecom TEXT,
                certificaciones_requeridas TEXT,
                
                -- Condiciones de contratación
                rango_salarial_min INTEGER,
                rango_salarial_max INTEGER,
                tipo_contrato TEXT,
                jornada TEXT,
                necesidad TEXT,
                
                -- Stakeholders
                responsable_seleccion TEXT,
                responsable_tecnico TEXT,
                hiring_manager TEXT,
                
                -- Cronograma
                fecha_apertura TEXT NOT NULL,
                fecha_cierre_estimada TEXT,
                fecha_cierre_real TEXT,
                
                -- Estado y KPIs
                estado TEXT DEFAULT 'abierta',
                time_to_hire INTEGER,
                candidatos_totales INTEGER DEFAULT 0,
                candidatos_finalistas INTEGER DEFAULT 0,
                candidato_seleccionado TEXT,
                
                -- Notas adicionales
                notas TEXT
            )
        ''')
        
        # ========================================
        # TABLA EVALUACIONES R/S/T - Sistema Alvatross
        # ========================================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidato_id TEXT NOT NULL,
                vacante_id TEXT,
                fecha TEXT NOT NULL,
                evaluador TEXT NOT NULL,
                
                -- Dimensión R: Entrevista/Comunicación (1-10)
                r_puntuacion INTEGER DEFAULT 0,
                r_notas TEXT,
                
                -- Dimensión S: Técnica/Stack (1-10)
                s_puntuacion INTEGER DEFAULT 0,
                s_notas TEXT,
                
                -- Dimensión T: Cultural/Soft Skills (1-10)
                t_puntuacion INTEGER DEFAULT 0,
                t_notas TEXT,
                
                -- Score final calculado
                score_final REAL DEFAULT 0.0,
                
                -- Señales de buen encaje (checklist)
                senales_encaje TEXT,
                
                -- Recomendación final
                recomendacion TEXT,
                
                -- Metadata
                tipo_entrevista TEXT,
                FOREIGN KEY (candidato_id) REFERENCES candidatos(id),
                FOREIGN KEY (vacante_id) REFERENCES vacantes(id)
            )
        ''')
        
        # ========================================
        # TABLA INTERACCIONES - Historial de contactos
        # ========================================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interacciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidato_id TEXT NOT NULL,
                fecha TEXT NOT NULL,
                tipo TEXT NOT NULL,
                responsable TEXT,
                notas TEXT,
                proximo_paso TEXT,
                FOREIGN KEY (candidato_id) REFERENCES candidatos(id)
            )
        ''')
        
        # ========================================
        # TABLA ASOCIACIÓN CANDIDATO-VACANTE
        # ========================================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidato_vacante (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidato_id TEXT NOT NULL,
                vacante_id TEXT NOT NULL,
                fase TEXT DEFAULT 'screening',
                fecha_asignacion TEXT NOT NULL,
                notas_fase TEXT,
                FOREIGN KEY (candidato_id) REFERENCES candidatos(id),
                FOREIGN KEY (vacante_id) REFERENCES vacantes(id),
                UNIQUE(candidato_id, vacante_id)
            )
        ''')
        
        self.disconnect()
    
    # ========================================
    # CRUD CANDIDATOS
    # ========================================
    
    def crear_candidato(self, datos):
        """Crear nuevo candidato"""
        cursor = self.connect()
        
        # Generar ID único basado en timestamp
        candidato_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        cursor.execute('''
            INSERT INTO candidatos (
                id, nombre, email, telefono, linkedin, github, localizacion,
                remoto, disponibilidad, carnet_conducir, vehiculo_propio,
                nivel_estudios, titulacion, certificaciones, idiomas,
                experiencia_total, experiencia_telecom, experiencia_tmforum,
                ultimo_puesto, ultima_empresa, proyectos,
                stack_lenguajes, stack_frameworks, stack_bbdd, stack_cloud,
                stack_devops, stack_apis, stack_mensajeria,
                competencias, salario_esperado, estado, perfil_it, seniority,
                gdpr_consent, fecha_registro, origen, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidato_id,
            datos.get('nombre'),
            datos.get('email'),
            datos.get('telefono'),
            datos.get('linkedin'),
            datos.get('github'),
            datos.get('localizacion'),
            datos.get('remoto'),
            datos.get('disponibilidad'),
            datos.get('carnet_conducir', 0),
            datos.get('vehiculo_propio', 0),
            datos.get('nivel_estudios'),
            datos.get('titulacion'),
            datos.get('certificaciones'),
            datos.get('idiomas'),
            datos.get('experiencia_total', 0),
            datos.get('experiencia_telecom', 0),
            datos.get('experiencia_tmforum'),
            datos.get('ultimo_puesto'),
            datos.get('ultima_empresa'),
            datos.get('proyectos'),
            datos.get('stack_lenguajes'),
            datos.get('stack_frameworks'),
            datos.get('stack_bbdd'),
            datos.get('stack_cloud'),
            datos.get('stack_devops'),
            datos.get('stack_apis'),
            datos.get('stack_mensajeria'),
            datos.get('competencias'),
            datos.get('salario_esperado'),
            'activo',
            datos.get('perfil_it'),
            datos.get('seniority'),
            datos.get('gdpr_consent', 0),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datos.get('origen', 'manual'),
            datos.get('notas', '')
        ))
        
        self.disconnect()
        return candidato_id
    
    def obtener_candidato(self, candidato_id):
        """Obtener un candidato por ID"""
        cursor = self.connect()
        cursor.execute('SELECT * FROM candidatos WHERE id = ?', (candidato_id,))
        resultado = cursor.fetchone()
        self.disconnect()
        return dict(resultado) if resultado else None
    
    def listar_candidatos(self, filtro_estado=None, buscar=None, perfil_it=None):
        """Listar todos los candidatos con filtros"""
        cursor = self.connect()
        
        query = "SELECT id, nombre, email, telefono, ultimo_puesto, stack_lenguajes, perfil_it, seniority, estado, fecha_registro FROM candidatos WHERE estado != 'archivado'"
        params = []
        
        if filtro_estado:
            query += " AND estado = ?"
            params.append(filtro_estado)
        
        if perfil_it:
            query += " AND perfil_it = ?"
            params.append(perfil_it)
        
        if buscar:
            query += " AND (nombre LIKE ? OR email LIKE ? OR stack_lenguajes LIKE ? OR ultimo_puesto LIKE ?)"
            buscar_param = f"%{buscar}%"
            params.extend([buscar_param, buscar_param, buscar_param, buscar_param])
        
        query += " ORDER BY fecha_registro DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        self.disconnect()
        
        return [dict(row) for row in resultados]
    
    def actualizar_candidato(self, candidato_id, datos):
        """Actualizar datos de un candidato"""
        cursor = self.connect()
        
        campos = []
        valores = []
        
        for campo, valor in datos.items():
            campos.append(f"{campo} = ?")
            valores.append(valor)
        
        valores.append(candidato_id)
        
        query = f"UPDATE candidatos SET {', '.join(campos)} WHERE id = ?"
        cursor.execute(query, valores)
        
        self.disconnect()
        return cursor.rowcount > 0
    
    def eliminar_candidato(self, candidato_id):
        """Archivar un candidato (no borrar)"""
        cursor = self.connect()
        cursor.execute('UPDATE candidatos SET estado = "archivado" WHERE id = ?', (candidato_id,))
        self.disconnect()
        return cursor.rowcount > 0
    
    # ========================================
    # CRUD VACANTES
    # ========================================
    
    def crear_vacante(self, datos):
        """Crear nueva vacante"""
        cursor = self.connect()
        
        # Generar ID único ALV-YYYY-NNN
        cursor.execute('SELECT COUNT(*) FROM vacantes WHERE id LIKE ?', (f"ALV-{datetime.now().year}%",))
        count = cursor.fetchone()[0] + 1
        vacante_id = f"ALV-{datetime.now().year}-{count:03d}"
        
        cursor.execute('''
            INSERT INTO vacantes (
                id, titulo, perfil_it, seniority, departamento, ubicacion, modalidad,
                stack_obligatorio, stack_deseable, experiencia_tmforum, experiencia_telecom,
                certificaciones_requeridas, rango_salarial_min, rango_salarial_max,
                tipo_contrato, jornada, necesidad, responsable_seleccion,
                responsable_tecnico, hiring_manager, fecha_apertura,
                fecha_cierre_estimada, estado, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vacante_id,
            datos.get('titulo'),
            datos.get('perfil_it'),
            datos.get('seniority'),
            datos.get('departamento'),
            datos.get('ubicacion'),
            datos.get('modalidad'),
            datos.get('stack_obligatorio'),
            datos.get('stack_deseable'),
            datos.get('experiencia_tmforum'),
            datos.get('experiencia_telecom'),
            datos.get('certificaciones_requeridas'),
            datos.get('rango_salarial_min'),
            datos.get('rango_salarial_max'),
            datos.get('tipo_contrato'),
            datos.get('jornada'),
            datos.get('necesidad'),
            datos.get('responsable_seleccion'),
            datos.get('responsable_tecnico'),
            datos.get('hiring_manager'),
            datetime.now().strftime("%Y-%m-%d"),
            datos.get('fecha_cierre_estimada'),
            'abierta',
            datos.get('notas', '')
        ))
        
        self.disconnect()
        return vacante_id
    
    def obtener_vacante(self, vacante_id):
        """Obtener una vacante por ID"""
        cursor = self.connect()
        cursor.execute('SELECT * FROM vacantes WHERE id = ?', (vacante_id,))
        resultado = cursor.fetchone()
        self.disconnect()
        return dict(resultado) if resultado else None
    
    def listar_vacantes(self, estado=None, perfil_it=None):
        """Listar vacantes con filtros"""
        cursor = self.connect()
        
        query = "SELECT * FROM vacantes"
        params = []
        
        condiciones = []
        if estado:
            condiciones.append("estado = ?")
            params.append(estado)
        if perfil_it:
            condiciones.append("perfil_it = ?")
            params.append(perfil_it)
        
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)
        
        query += " ORDER BY fecha_apertura DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        self.disconnect()
        
        return [dict(row) for row in resultados]
    
    def actualizar_vacante(self, vacante_id, datos):
        """Actualizar vacante"""
        cursor = self.connect()
        
        campos = []
        valores = []
        
        for campo, valor in datos.items():
            campos.append(f"{campo} = ?")
            valores.append(valor)
        
        valores.append(vacante_id)
        
        query = f"UPDATE vacantes SET {', '.join(campos)} WHERE id = ?"
        cursor.execute(query, valores)
        
        self.disconnect()
        return cursor.rowcount > 0
    
    def cerrar_vacante(self, vacante_id, candidato_seleccionado=None):
        """Cerrar una vacante"""
        cursor = self.connect()
        
        update_data = {
            'estado': 'cerrada_cubierta' if candidato_seleccionado else 'cerrada_cancelada',
            'fecha_cierre_real': datetime.now().strftime("%Y-%m-%d")
        }
        
        if candidato_seleccionado:
            update_data['candidato_seleccionado'] = candidato_seleccionado
        
        campos = [f"{k} = ?" for k in update_data.keys()]
        valores = list(update_data.values()) + [vacante_id]
        
        query = f"UPDATE vacantes SET {', '.join(campos)} WHERE id = ?"
        cursor.execute(query, valores)
        
        self.disconnect()
        return True
    
    # ========================================
    # EVALUACIONES R/S/T
    # ========================================
    
    def crear_evaluacion(self, datos):
        """Crear evaluación R/S/T"""
        cursor = self.connect()
        
        # Calcular score final según ponderación por perfil
        r = datos.get('r_puntuacion', 0)
        s = datos.get('s_puntuacion', 0)
        t = datos.get('t_puntuacion', 0)
        
        # Ponderación por perfil (según guía Alvatross)
        ponderacion = {
            'backend': (0.20, 0.60, 0.20),
            'devops': (0.20, 0.60, 0.20),
            'qa': (0.25, 0.50, 0.25),
            'solution_architect': (0.25, 0.50, 0.25),
            'product_owner': (0.30, 0.40, 0.30),
            'integrations': (0.20, 0.60, 0.20),
            'support': (0.30, 0.40, 0.30),
            'frontend': (0.25, 0.50, 0.25)
        }
        
        perfil = datos.get('perfil_it', 'backend')
        p_r, p_s, p_t = ponderacion.get(perfil, (0.25, 0.50, 0.25))
        
        score_final = round((r * p_r) + (s * p_s) + (t * p_t), 2)
        
        cursor.execute('''
            INSERT INTO evaluaciones (
                candidato_id, vacante_id, fecha, evaluador,
                r_puntuacion, r_notas,
                s_puntuacion, s_notas,
                t_puntuacion, t_notas,
                score_final, senales_encaje, recomendacion,
                tipo_entrevista
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datos.get('candidato_id'),
            datos.get('vacante_id'),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datos.get('evaluador'),
            r, datos.get('r_notas', ''),
            s, datos.get('s_notas', ''),
            t, datos.get('t_notas', ''),
            score_final,
            datos.get('senales_encaje', ''),
            datos.get('recomendacion', ''),
            datos.get('tipo_entrevista', 'general')
        ))
        
        # Actualizar estado del candidato si score > 7.0
        if score_final >= 7.0:
            self.actualizar_candidato(datos.get('candidato_id'), {'estado': 'entrevista'})
        
        self.disconnect()
        return cursor.lastrowid
    
    def obtener_evaluaciones_candidato(self, candidato_id):
        """Obtener historial de evaluaciones de un candidato"""
        cursor = self.connect()
        cursor.execute('''
            SELECT * FROM evaluaciones 
            WHERE candidato_id = ? 
            ORDER BY fecha DESC
        ''', (candidato_id,))
        resultados = cursor.fetchall()
        self.disconnect()
        
        return [dict(row) for row in resultados]
    
    def obtener_ultima_evaluacion(self, candidato_id, vacante_id=None):
        """Obtener última evaluación de un candidato (opcional por vacante)"""
        cursor = self.connect()
        
        if vacante_id:
            cursor.execute('''
                SELECT * FROM evaluaciones 
                WHERE candidato_id = ? AND vacante_id = ?
                ORDER BY fecha DESC LIMIT 1
            ''', (candidato_id, vacante_id))
        else:
            cursor.execute('''
                SELECT * FROM evaluaciones 
                WHERE candidato_id = ?
                ORDER BY fecha DESC LIMIT 1
            ''', (candidato_id,))
        
        resultado = cursor.fetchone()
        self.disconnect()
        return dict(resultado) if resultado else None
    
    # ========================================
    # INTERACCIONES
    # ========================================
    
    def agregar_interaccion(self, candidato_id, tipo, responsable, notas, proximo_paso=None):
        """Registrar una interacción con un candidato"""
        cursor = self.connect()
        
        cursor.execute('''
            INSERT INTO interacciones (
                candidato_id, fecha, tipo, responsable, notas, proximo_paso
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            candidato_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tipo,
            responsable,
            notas,
            proximo_paso
        ))
        
        # Actualizar estado automáticamente según tipo
        if tipo == "entrevista_tecnica":
            self.actualizar_candidato(candidato_id, {'estado': 'entrevista_tecnica'})
        elif tipo == "offer":
            self.actualizar_candidato(candidato_id, {'estado': 'offer'})
        
        self.disconnect()
    
    def obtener_interacciones(self, candidato_id):
        """Obtener historial de interacciones"""
        cursor = self.connect()
        cursor.execute('''
            SELECT * FROM interacciones 
            WHERE candidato_id = ? 
            ORDER BY fecha DESC
        ''', (candidato_id,))
        resultados = cursor.fetchall()
        self.disconnect()
        
        return [dict(row) for row in resultados]
    
    # ========================================
    # ASOCIACIÓN CANDIDATO-VACANTE
    # ========================================
    
    def asociar_candidato_vacante(self, candidato_id, vacante_id, fase='screening', notas=''):
        """Asociar candidato a vacante"""
        cursor = self.connect()
        
        cursor.execute('''
            INSERT OR REPLACE INTO candidato_vacante (
                candidato_id, vacante_id, fase, fecha_asignacion, notas_fase
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            candidato_id,
            vacante_id,
            fase,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            notas
        ))
        
        # Incrementar contador de candidatos en vacante
        cursor.execute('''
            UPDATE vacantes 
            SET candidatos_totales = candidatos_totales + 1 
            WHERE id = ?
        ''', (vacante_id,))
        
        self.disconnect()
        return True
    
    def actualizar_fase_candidato(self, candidato_id, vacante_id, nueva_fase, notas=''):
        """Actualizar fase de candidato en vacante"""
        cursor = self.connect()
        
        cursor.execute('''
            UPDATE candidato_vacante 
            SET fase = ?, notas_fase = ?
            WHERE candidato_id = ? AND vacante_id = ?
        ''', (nueva_fase, notas, candidato_id, vacante_id))
        
        self.disconnect()
        return cursor.rowcount > 0
    
    def obtener_candidatos_vacante(self, vacante_id, fase=None):
        """Obtener candidatos asociados a una vacante"""
        cursor = self.connect()
        
        query = '''
            SELECT c.*, cv.fase, cv.notas_fase, cv.fecha_asignacion
            FROM candidatos c
            JOIN candidato_vacante cv ON c.id = cv.candidato_id
            WHERE cv.vacante_id = ?
        '''
        params = [vacante_id]
        
        if fase:
            query += " AND cv.fase = ?"
            params.append(fase)
        
        query += " ORDER BY cv.fecha_asignacion DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        self.disconnect()
        
        return [dict(row) for row in resultados]
    
    # ========================================
    # EXPORTACIÓN
    # ========================================
    
    def exportar_csv_candidatos(self, ruta_salida):
        """Exportar candidatos a CSV"""
        candidatos = self.listar_candidatos()
        
        if not candidatos:
            return False
        
        with open(ruta_salida, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=candidatos[0].keys())
            writer.writeheader()
            writer.writerows(candidatos)
        
        return True
    
    def exportar_csv_vacantes(self, ruta_salida):
        """Exportar vacantes a CSV"""
        vacantes = self.listar_vacantes()
        
        if not vacantes:
            return False
        
        with open(ruta_salida, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=vacantes[0].keys())
            writer.writeheader()
            writer.writerows(vacantes)
        
        return True
