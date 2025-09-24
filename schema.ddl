BEGIN;
--
-- Create model Causa
--
CREATE TABLE "acciones_causa" ("id" char(32) NOT NULL PRIMARY KEY, "nombre" varchar(150) NOT NULL UNIQUE, "slug" varchar(170) NOT NULL UNIQUE, "descripcion" text NOT NULL);
--
-- Create model Habilidad
--
CREATE TABLE "acciones_habilidad" ("id" char(32) NOT NULL PRIMARY KEY, "nombre" varchar(120) NOT NULL UNIQUE, "slug" varchar(140) NOT NULL UNIQUE);
--
-- Create model Organizacion
--
CREATE TABLE "acciones_organizacion" ("id" char(32) NOT NULL PRIMARY KEY, "nombre" varchar(200) NOT NULL UNIQUE, "correo" varchar(254) NOT NULL, "telefono" varchar(20) NOT NULL, "sitio_web" varchar(200) NOT NULL, "descripcion" text NOT NULL);
--
-- Create model Ubicacion
--
CREATE TABLE "acciones_ubicacion" ("id" char(32) NOT NULL PRIMARY KEY, "nombre" varchar(150) NOT NULL, "direccion" varchar(250) NOT NULL, "ciudad" varchar(120) NOT NULL, "latitud" real NULL, "longitud" real NULL);
--
-- Create model User
--
CREATE TABLE "acciones_user" ("password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "id" char(32) NOT NULL PRIMARY KEY, "rol" varchar(3) NOT NULL, "telefono" varchar(20) NOT NULL, "ciudad" varchar(100) NOT NULL);
CREATE TABLE "acciones_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" char(32) NOT NULL REFERENCES "acciones_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "acciones_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" char(32) NOT NULL REFERENCES "acciones_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "acciones_user_habilidades" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" char(32) NOT NULL REFERENCES "acciones_user" ("id") DEFERRABLE INITIALLY DEFERRED, "habilidad_id" char(32) NOT NULL REFERENCES "acciones_habilidad" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Campana
--
CREATE TABLE "acciones_campana" ("id" char(32) NOT NULL PRIMARY KEY, "titulo" varchar(200) NOT NULL, "slug" varchar(230) NOT NULL UNIQUE, "descripcion" text NOT NULL, "fecha_inicio" date NOT NULL, "fecha_termino" date NOT NULL, "creada_por_id" char(32) NULL REFERENCES "acciones_user" ("id") DEFERRABLE INITIALLY DEFERRED, "organizacion_id" char(32) NOT NULL REFERENCES "acciones_organizacion" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "acciones_campana_causas" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "campana_id" char(32) NOT NULL REFERENCES "acciones_campana" ("id") DEFERRABLE INITIALLY DEFERRED, "causa_id" char(32) NOT NULL REFERENCES "acciones_causa" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Actividad
--
CREATE TABLE "acciones_actividad" ("id" char(32) NOT NULL PRIMARY KEY, "titulo" varchar(200) NOT NULL, "descripcion" text NOT NULL, "inicio" datetime NOT NULL, "termino" datetime NOT NULL, "cupos" integer unsigned NOT NULL CHECK ("cupos" >= 0), "estado" varchar(3) NOT NULL, "campana_id" char(32) NOT NULL REFERENCES "acciones_campana" ("id") DEFERRABLE INITIALLY DEFERRED, "ubicacion_id" char(32) NULL REFERENCES "acciones_ubicacion" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Participacion
--
CREATE TABLE "acciones_participacion" ("id" char(32) NOT NULL PRIMARY KEY, "estado" varchar(3) NOT NULL, "postulada_en" datetime NOT NULL, "aprobada_en" datetime NULL, "check_in" datetime NULL, "check_out" datetime NULL, "horas" decimal NOT NULL, "actividad_id" char(32) NOT NULL REFERENCES "acciones_actividad" ("id") DEFERRABLE INITIALLY DEFERRED, "usuario_id" char(32) NOT NULL REFERENCES "acciones_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create index acciones_ca_fecha_i_6622bd_idx on field(s) fecha_inicio, fecha_termino of model campana
--
CREATE INDEX "acciones_ca_fecha_i_6622bd_idx" ON "acciones_campana" ("fecha_inicio", "fecha_termino");
--
-- Create constraint campana_fechas_validas on model campana
--
CREATE TABLE "new__acciones_campana" ("id" char(32) NOT NULL PRIMARY KEY, "titulo" varchar(200) NOT NULL, "slug" varchar(230) NOT NULL UNIQUE, "descripcion" text NOT NULL, "fecha_inicio" date NOT NULL, "fecha_termino" date NOT NULL, "creada_por_id" char(32) NULL REFERENCES "acciones_user" ("id") DEFERRABLE INITIALLY DEFERRED, "organizacion_id" char(32) NOT NULL REFERENCES "acciones_organizacion" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "campana_fechas_validas" CHECK ("fecha_termino" >= ("fecha_inicio")));
INSERT INTO "new__acciones_campana" ("id", "titulo", "slug", "descripcion", "fecha_inicio", "fecha_termino", "creada_por_id", "organizacion_id") SELECT "id", "titulo", "slug", "descripcion", "fecha_inicio", "fecha_termino", "creada_por_id", "organizacion_id" FROM "acciones_campana";
DROP TABLE "acciones_campana";
ALTER TABLE "new__acciones_campana" RENAME TO "acciones_campana";
CREATE UNIQUE INDEX "acciones_user_groups_user_id_group_id_26bbe059_uniq" ON "acciones_user_groups" ("user_id", "group_id");
CREATE INDEX "acciones_user_groups_user_id_2146e03f" ON "acciones_user_groups" ("user_id");
CREATE INDEX "acciones_user_groups_group_id_b5a8ea41" ON "acciones_user_groups" ("group_id");
CREATE UNIQUE INDEX "acciones_user_user_permissions_user_id_permission_id_8b72f987_uniq" ON "acciones_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "acciones_user_user_permissions_user_id_427dbf39" ON "acciones_user_user_permissions" ("user_id");
CREATE INDEX "acciones_user_user_permissions_permission_id_0439c2e6" ON "acciones_user_user_permissions" ("permission_id");
CREATE UNIQUE INDEX "acciones_user_habilidades_user_id_habilidad_id_c75aeb08_uniq" ON "acciones_user_habilidades" ("user_id", "habilidad_id");
CREATE INDEX "acciones_user_habilidades_user_id_3a06b136" ON "acciones_user_habilidades" ("user_id");
CREATE INDEX "acciones_user_habilidades_habilidad_id_062995bd" ON "acciones_user_habilidades" ("habilidad_id");
CREATE UNIQUE INDEX "acciones_campana_causas_campana_id_causa_id_399c758a_uniq" ON "acciones_campana_causas" ("campana_id", "causa_id");
CREATE INDEX "acciones_campana_causas_campana_id_32f301c0" ON "acciones_campana_causas" ("campana_id");
CREATE INDEX "acciones_campana_causas_causa_id_c052192f" ON "acciones_campana_causas" ("causa_id");
CREATE INDEX "acciones_actividad_campana_id_24e67989" ON "acciones_actividad" ("campana_id");
CREATE INDEX "acciones_actividad_ubicacion_id_c2b90ed0" ON "acciones_actividad" ("ubicacion_id");
CREATE INDEX "acciones_participacion_actividad_id_071e456d" ON "acciones_participacion" ("actividad_id");
CREATE INDEX "acciones_participacion_usuario_id_3415b24f" ON "acciones_participacion" ("usuario_id");
CREATE INDEX "acciones_campana_creada_por_id_37b62730" ON "acciones_campana" ("creada_por_id");
CREATE INDEX "acciones_campana_organizacion_id_e63754d2" ON "acciones_campana" ("organizacion_id");
CREATE INDEX "acciones_ca_fecha_i_6622bd_idx" ON "acciones_campana" ("fecha_inicio", "fecha_termino");
--
-- Create index acciones_pa_estado_514ed6_idx on field(s) estado of model participacion
--
CREATE INDEX "acciones_pa_estado_514ed6_idx" ON "acciones_participacion" ("estado");
--
-- Alter unique_together for participacion (1 constraint(s))
--
CREATE UNIQUE INDEX "acciones_participacion_usuario_id_actividad_id_bf9758e8_uniq" ON "acciones_participacion" ("usuario_id", "actividad_id");
--
-- Create index acciones_ac_inicio_8d7436_idx on field(s) inicio of model actividad
--
CREATE INDEX "acciones_ac_inicio_8d7436_idx" ON "acciones_actividad" ("inicio");
--
-- Create index acciones_ac_estado_8dc631_idx on field(s) estado of model actividad
--
CREATE INDEX "acciones_ac_estado_8dc631_idx" ON "acciones_actividad" ("estado");
--
-- Create constraint actividad_tiempo_valido on model actividad
--
CREATE TABLE "new__acciones_actividad" ("id" char(32) NOT NULL PRIMARY KEY, "titulo" varchar(200) NOT NULL, "descripcion" text NOT NULL, "inicio" datetime NOT NULL, "termino" datetime NOT NULL, "cupos" integer unsigned NOT NULL CHECK ("cupos" >= 0), "estado" varchar(3) NOT NULL, "campana_id" char(32) NOT NULL REFERENCES "acciones_campana" ("id") DEFERRABLE INITIALLY DEFERRED, "ubicacion_id" char(32) NULL REFERENCES "acciones_ubicacion" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "actividad_tiempo_valido" CHECK ("termino" > ("inicio")));
INSERT INTO "new__acciones_actividad" ("id", "titulo", "descripcion", "inicio", "termino", "cupos", "estado", "campana_id", "ubicacion_id") SELECT "id", "titulo", "descripcion", "inicio", "termino", "cupos", "estado", "campana_id", "ubicacion_id" FROM "acciones_actividad";
DROP TABLE "acciones_actividad";
ALTER TABLE "new__acciones_actividad" RENAME TO "acciones_actividad";
CREATE INDEX "acciones_actividad_campana_id_24e67989" ON "acciones_actividad" ("campana_id");
CREATE INDEX "acciones_actividad_ubicacion_id_c2b90ed0" ON "acciones_actividad" ("ubicacion_id");
CREATE INDEX "acciones_ac_inicio_8d7436_idx" ON "acciones_actividad" ("inicio");
CREATE INDEX "acciones_ac_estado_8dc631_idx" ON "acciones_actividad" ("estado");
COMMIT;
