#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
database.py
Gestión de la base de datos SQLite para candidatos
"""

import sqlite3
from pathlib import Path
from datetime import datetime


class DatabaseManager:
    """Clase para manejar la conexión y operaciones con SQLite"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Carpeta data en el mismo directorio que el script
            data_dir = Path(__file__).parent / "data"
            data_dir.mkdir(exist_ok=True)
            self.db_path = data_dir / "candidatos.db"
        else:
            self.db_path = Path(db_path)
        
        self.conn = None
        self._create_tables()
    
    def connect(self):
        """Conectar a la base de datos"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
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
        
        # Tabla de candidatos
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
                nivel_estudios TEXT,
                titulacion TEXT,
                certificaciones TEXT,
                idiomas TEXT,
                experiencia_total INTEGER,
                experiencia_telecom INTEGER,
                ultimo_puesto TEXT,
                ultima_empresa TEXT,
                proyectos TEXT,
                experiencia_tmforum TEXT,
                stack_lenguajes TEXT,
                stack_frameworks TEXT,
                stack_bbdd TEXT,
                stack_cloud TEXT,
                stack_devops TEXT,
                stack_apis TEXT,
                stack_mensajeria TEXT,
                competencias TEXT,
                cv_path TEXT,
                portfolio TEXT,
                gdpr_consent BOOLEAN DEFAULT 0,
                fecha_registro TEXT,
                origen TEXT,
                estado TEXT DEFAULT 'activo',
                notas TEXT
            )
        ''')
        
        # Tabla de interacciones (historial de contactos)
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
        
        self.disconnect()
    
    # ==================== CRUD CANDIDATOS ====================
    
    def crear_candidato(self, datos):
        """Crear nuevo candidato"""
        cursor = self.connect()
        
        # Generar ID único basado en timestamp
        candidato_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        cursor.execute('''
            INSERT INTO candidatos (
                id, nombre, email, telefono, linkedin, github, localizacion,
                remoto, disponibilidad, nivel_estudios, titulacion, certificaciones,
                idiomas, experiencia_total, experiencia_telecom, ultimo_puesto,
                ultima_empresa, proyectos, experiencia_tmforum, stack_lenguajes,
                stack_frameworks, stack_bbdd, stack_cloud, stack_devops,
                stack_apis, stack_mensajeria, competencias, cv_path,
                portfolio, gdpr_consent, fecha_registro, origen, estado, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            datos.get('nivel_estudios'),
            datos.get('titulacion'),
            datos.get('certificaciones'),
            datos.get('idiomas'),
            datos.get('experiencia_total', 0),
            datos.get('experiencia_telecom', 0),
            datos.get('ultimo_puesto'),
            datos.get('ultima_empresa'),
            datos.get('proyectos'),
            datos.get('experiencia_tmforum'),
            datos.get('stack_lenguajes'),
            datos.get('stack_frameworks'),
            datos.get('stack_bbdd'),
            datos.get('stack_cloud'),
            datos.get('stack_devops'),
            datos.get('stack_apis'),
            datos.get('stack_mensajeria'),
            datos.get('competencias'),
            datos.get('cv_path'),
            datos.get('portfolio'),
            datos.get('gdpr_consent', False),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datos.get('origen', 'manual'),
            'activo',
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
    
    def listar_candidatos(self, filtro_estado=None, buscar=None):
        """Listar todos los candidatos (con filtros opcionales)"""
        cursor = self.connect()
        
        query = "SELECT id, nombre, email, telefono, ultimo_puesto, stack_lenguajes, estado, fecha_registro FROM candidatos WHERE estado != 'archivado'"
        params = []
        
        if filtro_estado:
            query += " AND estado = ?"
            params.append(filtro_estado)
        
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
        
        # Construir SET dinámicamente
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
        """Eliminar (archivar) un candidato"""
        cursor = self.connect()
        cursor.execute('UPDATE candidatos SET estado = "archivado" WHERE id = ?', (candidato_id,))
        self.disconnect()
        return cursor.rowcount > 0
    
    # ==================== INTERACCIONES ====================
    
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
        
        self.disconnect()
    
    def obtener_interacciones(self, candidato_id):
        """Obtener historial de interacciones de un candidato"""
        cursor = self.connect()
        cursor.execute('''
            SELECT * FROM interacciones 
            WHERE candidato_id = ? 
            ORDER BY fecha DESC
        ''', (candidato_id,))
        resultados = cursor.fetchall()
        self.disconnect()
        
        return [dict(row) for row in resultados]
    
    # ==================== EXPORTACIÓN ====================
    
    def exportar_csv(self, ruta_salida):
        """Exportar todos los candidatos activos a CSV"""
        import csv
        
        candidatos = self.listar_candidatos()
        
        if not candidatos:
            return False
        
        with open(ruta_salida, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=candidatos[0].keys())
            writer.writeheader()
            writer.writerows(candidatos)
        
        return True
