from .connection import DataBase


class Model(object):
    # Constructor de la clase y donde busco la tira de conexion (no se toca)
    def __init__(self, dsn):
        self.connection = DataBase(dsn)

    # ejemplo de creación de un metodo para una consulta
    def get_tablespaces(self):
        sql = """select
               a.tablespace_name,
               (nvl(b.tot_used,0)/a.bytes_alloc)*100 SPACE_USED
            from
               (select
                  tablespace_name,
                  sum(bytes) physical_bytes,
                  sum(decode(autoextensible,'NO',bytes,'YES',maxbytes)) bytes_alloc
                from
                  dba_data_files
                group by
                  tablespace_name ) a,
               (select
                  tablespace_name,
                  sum(bytes) tot_used
                from
                  dba_segments
                group by
                  tablespace_name ) b
            where
               a.tablespace_name = b.tablespace_name (+)
            and
               a.tablespace_name not in
               (select distinct
                   tablespace_name
                from
                   dba_temp_files)
            order by 2 desc
        """
        return self.connection.db_query(sql)

    def get_locked(self):
        sql = """SELECT DISTINCT
            SID,
            SERIAL#,
            ORACLE_USERNAME,
            OS_USER_NAME,
            LOCKED_MODE,
            s.STATUS,
            MACHINE,
            PROGRAM,
            OWNER,
            OBJECT_NAME,
            OBJECT_TYPE
        FROM v$session s 
          inner join v$locked_object lo
            on lo.PROCESS=s.PROCESS
          inner join v$lock l
            on l.LMODE=lo.LOCKED_MODE
          inner join dba_objects do 
            on do.OBJECT_ID=lo.OBJECT_ID
        WHERE s.sid=l.sid
          and (l.block=0 or l.block=1 and l.ctime/60>=10)
          and do.object_name!='REP$EJECFIN'
        """
        return self.connection.db_query(sql)

    def get_session_inactive(self):
        # sql = """SELECT username,
        #     machine,
        #     sid,
        #     serial#,
        #     status,
        #     to_char(logon_time, 'DD.MM.YYYY HH24:MI:SS') as logon_time,
        #     ((TRUNC(MOD((TO_DATE(to_char(current_timestamp, 'DD.MM.YYYY HH24:MI:SS'), 'DD.MM.YYYY HH24:MI:SS') - logon_time) * 24, 24))*60) + (TRUNC(MOD((TO_DATE(to_char(current_timestamp, 'DD.MM.YYYY HH24:MI:SS'), 'DD.MM.YYYY HH24:MI:SS') - logon_time) * (60 * 24), 60)))) as tiempo_de_inactividad
        #     FROM gv$session
        #     where status='INACTIVE' and
        #     ((TRUNC(MOD((TO_DATE(to_char(current_timestamp, 'DD.MM.YYYY HH24:MI:SS'), 'DD.MM.YYYY HH24:MI:SS') - logon_time) * 24, 24))*60) + (TRUNC(MOD((TO_DATE(to_char(current_timestamp, 'DD.MM.YYYY HH24:MI:SS'), 'DD.MM.YYYY HH24:MI:SS') - logon_time) * (60 * 24), 60))))>=30 order by logon_time asc
        # """
        sql = """SELECT count(sid) FROM gv$session
            where status='INACTIVE' and
            ((TRUNC(MOD((TO_DATE(to_char(current_timestamp, 'DD.MM.YYYY HH24:MI:SS'), 'DD.MM.YYYY HH24:MI:SS') - logon_time) * 24, 24))*60) + (TRUNC(MOD((TO_DATE(to_char(current_timestamp, 'DD.MM.YYYY HH24:MI:SS'), 'DD.MM.YYYY HH24:MI:SS') - logon_time) * (60 * 24), 60))))>=30 order by logon_time asc
        """
        return self.connection.db_query(sql)

    def get_collection_banks(self):
        sql = """select 
            BR.NOMBRE_BANCO banco,  count(mp.ID_MOVIMIENTO_PAGO) cantidad
            from KBLANCOA.BANCO_RECAUDA BR 
            right join DBO.MOVIMIENTO_PAGO  partition (P_2022_Q1) mp 
            on (BR.CODIGO_BANCO = mp.BANCO_PAGO)
            where 
            TRUNC(FECHA_RECAUDACION_PAGO) = TRUNC(SYSDATE) -1 
            and ORIGEN_INFORMACION_PAGO = '32'
            group by BR.NOMBRE_BANCO
            order by count(2) desc
        """
        return self.connection.db_query(sql)