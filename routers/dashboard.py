
from fastapi import APIRouter


dashboard_router = APIRouter( prefix = "/dashboard", tags = ["dashboard"] )

# @app.get("/dashboard")
# def get_quant_metrics():

#     with Session(engine) as session:

#         finished_total_games = session.exec( select( func.count(Game.id) ).where( Game.finished ) ).first()
#         winning_total_games = session.exec( select( Game.winner, func.count(Game.id) ).where( Game.finished, Game.draw == False ).group_by( Game.winner ) ).fetchall()
#         draw_total_games = session.exec( select( func.count(Game.id) ).where( Game.draw ) ).first()
        
#         return JSONResponse(
#             {
#                 "totalFinished": finished_total_games,
#                 "totalWinning": [ {"player": player, "playerTotalWinning": total } for player, total in winning_total_games],
#                 "totalDraw": draw_total_games
#             }, 
#             status_code = 200 
#         )