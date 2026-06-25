from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllAlbum(minuti):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """with minuti_album as (
                    select t.AlbumId as album, sum(t.Milliseconds)/60000 minuti_tot
                    from track t
                    group by t.AlbumId
                    having minuti_tot >= %s
                    )
                select a.*, m.minuti_tot as Durata
                from minuti_album m
                join album a on m.album = a.AlbumId
                order by a.Title"""
        cursor.execute(query, (minuti,))
        for row in cursor:
            results.append(Album(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(minuti, idMapA):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """with minuti_album as (
                    select t.AlbumId as album, p.PlaylistId as playlist, sum(t.Milliseconds)/(60000) minuti_tot
                    from track t
                    join playlisttrack p on p.TrackId = t.TrackId 
                    group by t.AlbumId, p.PlaylistId 
                    having minuti_tot >= %s
                    )
                select a.album as id1, a2.album as id2
                from minuti_album a
                join minuti_album a2 on a2.playlist = a.playlist 
                where a.album < a2.album"""
        cursor.execute(query,(minuti,))
        for row in cursor:
            results.append((idMapA[row['id1']], idMapA[row['id2']]))
        cursor.close()
        conn.close()
        return results