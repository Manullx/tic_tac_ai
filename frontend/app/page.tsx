import { getGame } from "@/app/lib/api"

import Board from "@/app/components/board"

export default async function Game() {
  
  const { game_id } = await getGame();
  
  return (
    <div>
      <div className="flex justify-center p-2">
        Game ID: { game_id }
      </div>
      <Board game_id={game_id}/>
    </div>
  )
}