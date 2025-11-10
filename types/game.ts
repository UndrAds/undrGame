export interface Game {
  slug: string;
  url: string;
  title: string;
  img: string;
}

export interface GameWithCategory extends Game {
  category: string;
}
