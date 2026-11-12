# APP RECRUITING ALVATROSS - ESQUEMA COMPLETO
*Última actualización: 31/01/2026 | Grupo SATEC - Alvatross*

---

## 📁 MÓDULO 01: BASE DE DATOS DE CANDIDATOS

### Ficha Candidato
- **ID_Candidato**: UUID autogenerado
- **Datos Personales**
  - Nombre_Completo
  - Email
  - Teléfono
  - LinkedIn_URL
  - GitHub_URL / GitLab_URL
  - Localización (País, Provincia, Ciudad)
  - Disponibilidad_Remoto (Total / Parcial / Presencial)
  - Disponibilidad_Incorporación (Inmediata / 15d / 30d / 60d+)
  - Carnet_Conducir (Sí / No)
  - Vehículo_Propio (Sí / No)
- **Formación**
  - Nivel_Estudios (Grado / Máster / Doctorado / FP)
  - Titulación
  - Certificaciones_Relevantes (lista)
  - Idiomas (nivel CERF)
- **Experiencia Profesional**
  - Total_Años_IT
  - Total_Años_Telecom/OSS/BSS
  - Último_Puesto
  - Última_Empresa
  - Proyectos_Relevantes (lista con stack y duración)
  - Experiencia_TMForum_ODA (Sí / No / Nivel)
- **Stack Técnico (matriz ponderada)**
  - Lenguajes_Programación
    - Java (Nivel: Junior / Mid / Senior / Expert)
    - Python (Nivel: ...)
    - Node.js (Nivel: ...)
    - Go (Nivel: ...)
    - TypeScript (Nivel: ...)
  - Frameworks_Backend
    - Spring_Boot
    - Django
    - Express
  - Frameworks_Frontend
    - Angular
    - React
  - Bases_Datos
    - SQL (Oracle / PostgreSQL / MySQL)
    - NoSQL (MongoDB / Cassandra)
  - Cloud_Platforms
    - AWS
    - Azure
    - GCP
  - DevOps_Tools
    - Docker
    - Kubernetes / OpenShift
    - Terraform
    - Ansible
    - GitLab_CI / Jenkins
  - APIs_Integración
    - REST
    - TMForum_OpenAPIs
    - SOAP
    - GraphQL
  - Mensajería
    - Kafka
    - RabbitMQ
- **Competencias Blandas**
  - Comunicación_Técnica
  - Trabajo_en_Equipo
  - Resolución_Problemas
  - Adaptabilidad
  - Ownership
- **Adjuntos**
  - CV_PDF (enlace/encriptado)
  - Portfolio_URL
  - Certificados (lista enlaces)
- **Metadata Privacidad**
  - Fecha_Registro
  - Consentimiento_GDPR (Sí / No + fecha)
  - Origen_Captación (LinkedIn / Referido / JobBoard / Otro)
  - Última_Actualización
  - Estado_Activo (Activo / Inactivo / Archivado)

### Historial Interacciones
- Fecha_Interacción
- Tipo (Email / Entrevista / Call / LinkedIn / Otro)
- Responsable_RRHH
- Notas (texto libre + etiquetas)
- Próximo_Paso (fecha + acción)

### Búsqueda Avanzada
- Filtros_Múltiples (AND / OR)
- Búsqueda_Semántica (stack + perfil)
- Exportar_Listado (CSV / Excel)
- Etiquetas_Custom (ej: "urgente", "recomendado", "en_standby")

---

## 📁 MÓDULO 02: GESTIÓN DE VACANTES

### Ficha Vacante
- **ID_Vacante**: ALV-YYYY-NNN (ej: ALV-2026-042)
- **Datos Básicos**
  - Título_Puesto (ej: "Backend Developer - Java/Spring")
  - Perfil_Tipo (Backend / DevOps / QA / Cloud / Integrations / SA / PO / Support / Frontend)
  - Seniority_Requerido (Junior / Mid / Senior / Lead)
  - Departamento (Desarrollo / DevOps / Producto / Arquitectura / Operaciones)
  - Tipo_Necesidad (Nueva / Reemplazo)
  - Motivo_Reemplazo (opcional, texto libre)
- **Requisitos Técnicos**
  - Stack_Obligatorio (lista con niveles mínimos)
  - Stack_Deseable (lista con niveles)
  - Experiencia_TMForum_ODA (Obligatorio / Deseable / No_relevante)
  - Experiencia_Telecom (Obligatorio / Deseable / No_relevante)
  - Certificaciones_Requeridas (ej: AWS / Azure / ISO27001 / ENS)
- **Condiciones Contratación**
  - Modalidad (Remoto_Total / Remoto_Parcial / Presencial)
  - Ubicación_Oficina (Madrid / Avilés / Indistinto)
  - Rango_Salarial_Min (EUR)
  - Rango_Salarial_Max (EUR)
  - Tipo_Contrato (Indefinido / Temporal)
  - Jornada (Completa / Parcial)
- **Stakeholders**
  - Responsable_Selección (RRHH)
  - Responsable_Técnico (Tech Lead / Arquitecto)
  - Hiring_Manager (Jefe de Área)
  - Aprobador_Final (Director)
- **Cronograma**
  - Fecha_Apertura
  - Fecha_Cierre_Estimada
  - Fecha_Cierre_Real
  - Deadline_Urgente (Sí / No + fecha)
- **Estado Vacante**
  - Estado (Abierta / En_proceso / Cerrada_Cancelada / Cerrada_Cubierta)
  - Razón_Cierre (Cubierta / Cancelada_Cambio_Prioridad / Vacante_Desaparecida / Otro)
- **KPI Vacante**
  - Time_to_Hire (días)
  - Cost_per_Hire (EUR)
  - Nº_Candidatos_Totales
  - Nº_Entrevistas_Realizadas

### Pipeline Candidatos (vista Kanban)
- Etapa_01: Sourcing (candidatos identificados)
- Etapa_02: Screening_Telefónico (entrevista RRHH)
- Etapa_03: Entrevista_Técnica (Tech Lead / Arquitecto)
- Etapa_04: Entrevista_Cultural (Hiring Manager)
- Etapa_05: Finalistas (top 3)
- Etapa_06: Offer (enviada / aceptada / rechazada)
- Etapa_07: Onboarding (incorporado)
- **Funcionalidades**
  - Visualización_Kanban (drag&drop entre etapas)
  - Alertas_Automáticas (etapa estancada >7 días)

### Finalistas y Seleccionados
- Candidato_Finalista_01 (ID + nombre + score_final)
- Candidato_Finalista_02 (ID + nombre + score_final)
- Candidato_Finalista_03 (ID + nombre + score_final)
- Candidato_Seleccionado (ID + nombre + fecha_aceptación)
- Feedback_Rechazados (notas por candidato)

---

## 📁 MÓDULO 03: EVALUACIÓN AUTOMÁTICA (R/S/T)

### Rúbrica RST Alvatross
- **Dimensión R (Entrevista / Comunicación)**
  - Puntuación (1-10)
  - Criterios Guía:
    - 1-3: respuestas vagas, sin ejemplos, confusión conceptos base
    - 4-6: base correcta, algunos ejemplos, huecos puntuales
    - 7-8: sólido, ejemplos claros, buena toma decisiones
    - 9-10: excelente, liderazgo/ownership, profundidad, anticipa riesgos
  - Notas_Evaluador (texto libre)
- **Dimensión S (Técnica / Stack)**
  - Puntuación (1-10)
  - Criterios por perfil específico (Backend, DevOps, QA, etc.)
  - Notas_Evaluador
  - Ejercicio_Práctico (Sí / No + resultado + enlace repositorio)
- **Dimensión T (Cultural / Soft Skills)**
  - Puntuación (1-10)
  - Criterios:
    - Alineación con DevSecOps / cloud-native
    - Colaboración equipos multidisciplinares
    - Estabilidad / proyectos larga duración
    - Explicación decisiones técnicas con claridad
  - Notas_Evaluador

### Cálculo Score Automático
- **Ponderación por Rol (configurable)**
  - Backend: R(20%) + S(60%) + T(20%)
  - DevOps: R(20%) + S(60%) + T(20%)
  - QA: R(25%) + S(50%) + T(25%)
  - Solution Architect: R(25%) + S(50%) + T(25%)
  - Product Owner: R(30%) + S(40%) + T(30%)
  - Integrations: R(20%) + S(60%) + T(20%)
  - Support: R(30%) + S(40%) + T(30%)
- **Fórmula**: `Score_Final = (R * P_R) + (S * P_S) + (T * P_T)`
- **Umbral Mínimo Aprobación** (configurable por rol)
- **Bandas Automáticas**
  - 🔴 Rojo (<5.0): descartar
  - 🟡 Amarillo (5.0-6.9): evaluar con precaución
  - 🟢 Verde (7.0-8.4): buen candidato
  - 🔵 Azul (8.5-10.0): top talent

### Señales de Buen Encaje (checklist por perfil)
- **Backend**
  - [ ] Explica decisiones técnicas con datos
  - [ ] Piensa en resiliencia (timeouts/retries/circuit breakers)
  - [ ] Conoce prácticas calidad (tests unitarios/integración, code review)
- **DevOps**
  - [ ] Automatiza por defecto (IaC, pipelines)
  - [ ] Enfoca seguridad sin bloquear entregas (DevSecOps)
- **QA**
  - [ ] Pensamiento crítico y precisión en reporte bugs
  - [ ] Colabora como habilitador (no policía de calidad)
- **Solution Architect**
  - [ ] Visión sistémica y criterio técnico sólido
  - [ ] Documentación útil y comunicación impecable
- **Product Owner**
  - [ ] Claridad, estructura, foco en valor de negocio
  - [ ] Respeta límites técnicos y capacidad equipo
- **Integrations/API Specialist**
  - [ ] Precisión en contratos APIs y análisis logs
  - [ ] Piensa interoperabilidad desde diseño
- **Operations/Support**
  - [ ] Calma bajo presión y método sistemático
  - [ ] Documenta para evitar recurrencias

---

## 📁 MÓDULO 04: COMPARADOR MULTICANDIDATO

### Selección Candidatos
- Mínimo: 2 candidatos
- Máximo: ilimitado (recomendado ≤5 para visualización óptima)
- Origen: misma vacante / candidatos guardados / búsqueda libre

### Matriz Comparativa
| Campo Comparación          | Candidato A | Candidato B | Candidato C | ... |
|---------------------------|-------------|-------------|-------------|-----|
| Score Final RST           | 8.2         | 7.5         | 9.1         |     |
| Stack Java (nivel/años)   | Senior/5    | Mid/3       | Expert/8    |     |
| Kubernetes (nivel/años)   | Mid/2       | Senior/4    | Senior/4    |     |
| TMForum/ODA (Sí/No/años)  | Sí/3        | No          | Sí/6        |     |
| Telecom OSS/BSS (años)    | 4           | 1           | 7           |     |
| Inglés (nivel)            | C1          | B2          | C2          |     |
| Disponibilidad Incorporación | 15d      | Inmediata   | 30d         |     |
| Expectativas Salariales   | 42k         | 38k         | 48k         |     |
| Riesgo Fuga               | Medio       | Bajo        | Alto        |     |

### Destacado de Diferencias
- Resaltado automático:
  - ✅ Verde: ventaja significativa (+2 niveles o +3 años experiencia)
  - ❌ Rojo: carencia crítica (no cumple stack obligatorio)
  - ⚠️ Amarillo: diferencia moderada
- Filtro Prioridad: mostrar solo diferencias críticas

### Ranking Automático
- Ordenar por Score Final (descendente)
- Ordenar por Afinidad Stack (pesos personalizables)
- Exportar Ranking (PDF / Excel)

---

## 📁 MÓDULO 05: BANCO DE PREGUNTAS DE ENTREVISTA

### Preguntas Generales
- Identificación Datos Básicos (9 preguntas)
- Experiencia General (6 preguntas)
- Encaje Cultural (6 preguntas)
- Situacionales Behavioral (4 preguntas)

### Preguntas por Perfil Técnico
#### Backend / Full-Stack Developer
- Técnicas Core (7 preguntas sobre Java/Spring, microservicios, resiliencia)
- Ejercicio Práctico: "latencia alta en endpoint crítico"

#### Front-End Developer
- Técnicas Core (5 preguntas sobre Angular/React, rendimiento)
- Ejercicio Práctico: "optimización componente lento"

#### DevOps / Cloud / Security Engineer
- Técnicas Core (5 preguntas sobre IaC, Kubernetes, seguridad cloud)
- Ejercicio Práctico: "incidente producción - caída servicio"

#### QA / Automation Engineer
- Técnicas Core (5 preguntas sobre testing estrategias, frameworks)
- Ejercicio Práctico: "bug crítico detectado pre-despliegue"

#### Solution / Software Architect
- Arquitectura Core (6 preguntas sobre patrones, escalabilidad)
- Ejercicio Práctico: "diseño sistema alta transaccionalidad telecom"

#### Product Owner / Manager
- Producto Core (5 preguntas sobre backlog, priorización)
- Ejercicio Práctico: "priorización con recursos limitados"

#### Integrations / API Specialist
- Integración Core (5 preguntas sobre TMForum APIs, contratos)
- Ejercicio Práctico: "APIs incompatibles entre sistemas legacy"

#### Operations / Support Engineer
- Operaciones Core (4 preguntas sobre incidentes, SLAs)
- Ejercicio Práctico: "incidente crítico horario cliente internacional"

### Gestión de Preguntas
- Crear Nueva Pregunta (texto + etiquetas perfil/tecnología)
- Etiquetar por Tecnología (ej: "Kubernetes", "TMForum", "Spring")
- Marcar Favoritas (por entrevistador)
- Exportar Guía Entrevista (PDF personalizado por vacante)

---

## 📁 MÓDULO 06: METODOLOGÍAS ÁGILES

### Resumen Metodologías
- Scrum (roles, artefactos, eventos, duración sprints)
- Kanban (principios WIP, lead time, tablero)
- Lean (7 principios, eliminación waste)
- XP (prácticas TDD, pair programming, CI)
- Crystal (ajuste por tamaño/criticidad proyecto)
- FDD (phases por feature)
- DSDM (principios negocio + tiempo)
- AUP (fases RUP ágil)
- Scrumban (híbrido Scrum+Kanban)
- SAFe (escalado niveles: Team / Program / Portfolio)

### Uso en RRHH / Recruiting
- Preguntas Entrevista Ágil (para evaluar experiencia real)
- Checklist Evaluación Ágil:
  - [ ] Ha participado en ceremonias Scrum (daily, planning, retro)
  - [ ] Gestiona backlog personal o de equipo
  - [ ] Trabaja con Definition of Done
  - [ ] Valora retrospectivas como mejora continua
- Ejemplos Reales para Pedir: "cuéntame un sprint donde falló algo y cómo lo resolvisteis"

---

## 📁 MÓDULO 07: MARCO LEGAL ESPAÑA

### Convenio Colectivo Oficinas Madrid
- Tabla Salarial Actualizada (grupos profesionales + complementos)
- Jornada y Horarios (flexibilidad, cómputo anual)
- Vacaciones y Permisos (días, justificación)
- Plus Transporte / Alimentación (importe actual)
- Actualizaciones Automáticas (notificación cambios normativos)

### Estatuto de los Trabajadores
- Artículos Relevantes RRHH (selección práctica):
  - Contratación (tipos, duración, renovación)
  - Extinción Contrato (causas, indemnizaciones)
  - Derechos y Deberes
  - Vacaciones y Ausencias
  - Jornada y Descansos

### Cumplimiento GDPR / LOPD-GDD
- Registro Actividades Tratamiento (art. 30 RGPD)
- Consentimientos Candidatos (registro fechas + scope)
- Derecho Olvido (procedimiento archivado a los 2 años)
- Retención Datos (plazos legales: 2 años post-proceso)
- Plantilla Aviso Privacidad (para emails RRHH)

---

## 📁 MÓDULO 08: EMPRESA ALVATROSS (Grupo SATEC)

### Presentación Corporativa
- Quiénes Somos (misión, historia, pertenencia Grupo SATEC)
- Plataforma OSS Alvatross (características cloud-native, TMForum, ODA)
- Stack Tecnológico
  - Microservicios (Java/Spring Boot)
  - APIs TMForum Open APIs (SID, Party, Product)
  - Bases de Datos (Oracle, PostgreSQL)
  - Cloud (AWS, Azure)
  - DevSecOps (GitLab CI, Kubernetes, SonarQube)
- Clientes y Alcance (geografía, casos uso telecom)
- Oficinas (Madrid Aravaca, Avilés)
- Cultura (colaborativa, DevSecOps, Great Place to Work)
- Qué Buscamos (perfil ideal candidato IT/telecom)
- Qué Ofrecemos (estabilidad, proyectos internacionales, formación)

### Script Telefónico Entrevista
- Guion Inicial (presentación + objetivo llamada)
- Guion Cierre (próximos pasos + FAQ candidato)
- Plantilla Email Seguimiento (post-entrevista)

---

## 📁 MÓDULO 09: PERFILES HABITUALES IT / TELECOM

### Fichas Detalladas Roles (estructura común)
Para cada rol:
- Área (Desarrollo Producto / Ingeniería Software / Operaciones)
- Resumen Objetivo (2-3 líneas)
- Responsabilidades Principales (6 items)
- Requisitos Técnicos (6 items obligatorios + deseables)
- Soft Skills (5 items)
- Seniority (criterios Junior / Mid / Senior)
- Cultura Forma Trabajar (DevSecOps, colaboración)
- KPI Criterios Éxito (ej: tiempo resolución incidencias, calidad código)

#### Roles Incluidos
- Backend / Full-Stack Developer
- Front-End Developer
- DevOps / Cloud / Security Engineer
- QA / Automation Engineer
- Integrations / API Specialist
- Solution / Software Architect
- Product Owner / Manager
- Operations / Support Engineer

### Chuleta Rápida Stack
| Rol                          | Área               | Tecnologías Principales                     | Objetivo Principal                     |
|-----------------------------|--------------------|---------------------------------------------|----------------------------------------|
| Backend                     | Desarrollo         | Java, Spring Boot, PostgreSQL, Kafka        | Microservicios robustos y escalables   |
| DevOps                      | Ingeniería         | Kubernetes, Terraform, AWS, GitLab CI       | Automatización y resiliencia           |
| QA                          | Calidad            | Selenium, Cypress, JUnit, Postman           | Calidad sin bloquear velocidad         |
| Integrations                | Conectividad       | TMForum APIs, REST, SOAP, Kafka             | Interoperabilidad sistemas OSS/BSS     |
| Solution Architect          | Arquitectura       | Patrones, ODA, Cloud, Seguridad             | Diseño sistémico y gobernanza técnica  |
| Product Owner               | Producto           | Backlog, User Stories, Métricas             | Valor de negocio + viabilidad técnica  |
| Support                     | Operaciones        | SLAs, Incidentes, Logs, Documentación       | Estabilidad y resolución rápida        |

---

## 📁 MÓDULO 10: GLOSARIO DE TÉRMINOS

### Términos Técnicos IT / Telecom
- OSS/BSS (definición + contexto Alvatross)
- TMForum Open APIs (SID, Party, Product Ordering)
- ODA (Open Digital Architecture)
- Cloud Native (12-factor apps, microservicios)
- Microservicios (arquitectura, resiliencia)
- DevSecOps (integración seguridad en pipeline)
- CI/CD (Continuous Integration / Delivery)
- IaC (Infrastructure as Code)
- SLA / SLO / SLI (acuerdos nivel servicio)
- ... (todos términos relevantes stack Alvatross)

### Términos RRHH / Recruiting
- Sourcing (búsqueda activa candidatos)
- Screening (filtrado inicial)
- Time to Hire (días desde apertura hasta aceptación offer)
- Cost per Hire (coste total proceso selección)
- Offer Stage (fase envío propuesta)
- Onboarding (incorporación estructurada)
- Retention (retención talento)
- Employer Branding (marca empleadora)

---

## 📁 MÓDULO 11: LISTA DE TAREAS Y WORKFLOW RRHH

### Lista Tareas Personal
- Tareas Pendientes (con fecha límite y prioridad)
- Tareas En Progreso (estado %)
- Tareas Completadas (histórico + fecha cierre)
- Recordatorios Automáticos (email/app push 24h antes)

### Calendario Entrevistas
- Vista Día / Semana / Mes
- Bloques Disponibilidad Entrevistadores (Tech Leads, HM)
- Reserva Automática (evita conflictos horarios)
- Notificaciones Participantes (24h y 1h antes)
- Enlace Videollamada (Zoom / Teams autogenerado)

---

## 📁 MÓDULO 12: ONBOARDING POST-SELECCIÓN

### Checklist Incorporación
- **Pre Incorporación (D-7)**
  - [ ] Contrato firmado
  - [ ] Equipo IT asignado (portátil, cuenta correo)
  - [ ] Cuentas creadas (GitLab, Jira, Confluence, AWS)
  - [ ] Acceso oficina (tarjeta, parking)
- **Día 1**
  - [ ] Bienvenida equipo RRHH
  - [ ] Presentación equipo técnico
  - [ ] Documentación onboarding (guías, normas)
  - [ ] Primer café con mentor/tutor
- **Semana 1**
  - [ ] Formación producto Alvatross
  - [ ] Acceso repositorios y documentación técnica
  - [ ] Primer ticket/tarea asignada (low risk)
  - [ ] Reunión 1:1 con Tech Lead
- **Mes 1**
  - [ ] Revisión 30 días (feedback inicial)
  - [ ] Objetivos primer trimestre definidos
  - [ ] Feedback 360° inicial
- **Mes 3**
  - [ ] Evaluación 90 días formal
  - [ ] Alineación objetivos primer año
  - [ ] Plan desarrollo carrera

### Feedback Hiring Manager
- Formulario Estructurado (30 / 60 / 90 días)
- Puntuación Alineación Esperada vs Realidad (1-10)
- Comentarios Libres
- Alertas Riesgo Retention (si puntuación <6)

---

## 📁 MÓDULO 13: REPORTING Y ANALYTICS

### Dashboards Ejecutivos
- Pipeline Vacantes (abiertas vs cerradas vs en pausa)
- Time to Hire Promedio (últimos 6 meses, por rol)
- Source of Hire (% LinkedIn / Referido / JobBoard / Otro)
- Retention 90d (tasa éxito incorporaciones)
- Cost per Hire vs Budget (desviación %)
- Satisfaction Hiring Managers (NPS entrevistadores)

### Exportación Datos
- Reporte Mensual RRHH (PDF / Excel)
- Exporte Candidatos (CSV con GDPR compliance)
- Audit Trail (todas acciones en sistema: quién, cuándo, qué)

---

## 📁 MÓDULO 14: CONFIGURACIÓN DEL SISTEMA

### Usuarios y Permisos
- Roles:
  - RRHH_Admin (full access)
  - RRHH_Básico (lectura/escritura candidatos, no borrado)
  - Tech_Lead (evaluación técnica, no acceso salarios)
  - Hiring_Manager (ver finalistas, no sourcing)
- Permisos por Rol (matriz CRUD)
- Auditoría Accesos (registro login y acciones sensibles)

### Ponderaciones Personalizadas
- RoleWeights (tabla editable por perfil)
- Umbral Mínimo Score (configurable global o por vacante)
- Etiquetas Custom (creación/modificación)

### Integraciones Externas
- API LinkedIn Recruiter (búsqueda candidatos)
- Webhook GitHub/GitLab (verificación perfil técnico pública)
- Calendly / Outlook 365 (sincronización entrevistas)
- Slack / Teams (notificaciones equipo RRHH)
- BambooHR / Factorial (sincronización empleados actuales)

---

## ⚙️ NOTAS DE IMPLEMENTACIÓN

### Requisitos Técnicos
- Base de datos: PostgreSQL 14+ (encriptación campos sensibles: CV, emails)
- Autenticación: SSO con Azure AD (integración Grupo SATEC)
- Hosting: On-premise en infraestructura SATEC (cumplimiento GDPR)
- Backups: Diarios incrementales + semanales completos (retención 7 años)
- Accesibilidad: WCAG 2.1 AA (contraste, lectores pantalla)
- Multiidioma: ES / EN (toggle en cabecera)
- Responsive: Accesible desde móvil/tablet (entrevistas fuera oficina)

### Cumplimiento Legal
- GDPR / LOPD-GDD: consentimientos explícitos, derecho olvido automático a los 24 meses
- Retención datos candidatos: 24 meses desde último contacto
- Audit Trail completo para inspección laboral
- Encriptación en tránsito (TLS 1.3) y en reposo (AES-256)

### Roadmap Sugerido (Fases)
1. **Fase 1**: Módulos 01 + 02 + 05 (base operativa)
2. **Fase 2**: Módulo 03 (scoring automático) + Módulo 04 (comparador)
3. **Fase 3**: Módulos 07 + 08 + 11 (legal + empresa + tareas)
4. **Fase 4**: Módulos 09 + 10 + 12 (perfiles + glosario + onboarding)
5. **Fase 5**: Módulos 06 + 13 + 14 (agile + analytics + configuración)
