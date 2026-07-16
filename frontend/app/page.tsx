import { getGame } from "@/app/lib/api"

import Board from "@/app/components/board"

export default async function Game() {
  
  const { game_id } = await getGame();
  
  return (
    <div>
      <Board game_id={game_id}/>
    </div>
  )
}