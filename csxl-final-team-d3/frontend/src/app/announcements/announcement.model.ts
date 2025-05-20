import { PublicProfile } from '../profile/profile.service';

export interface Announcement {
  id: number | null;
  headline: string;
  synopsis: string;
  main_story: string;
  organization: string | null;
  state: State;
  slug: string;
  image: string | null;
  publish: string;
  modification: string;
  author_id: number | null;
}

export enum State {
  Draft = 'Draft',
  Published = 'Published',
  Archived = 'Archived'
}
