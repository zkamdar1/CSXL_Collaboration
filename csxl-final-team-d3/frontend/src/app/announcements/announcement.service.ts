import { EventEmitter, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Announcement, State } from './announcement.model';
import { Profile } from '../models.module';
import { Organization } from '../organization/organization.model';
import { Observable, ReplaySubject, tap, toArray } from 'rxjs';
import { PublicProfile } from '../profile/profile.service';

@Injectable({
  providedIn: 'root'
})
export class AnnouncementService {
  private announcements: ReplaySubject<Announcement[]> = new ReplaySubject(1);
  announcements$: Observable<Announcement[]> =
    this.announcements.asObservable();
  private fromWidgetDelete: boolean = false;
  public changes = new EventEmitter<void>();
  id: number = 5;

  constructor(private http: HttpClient) {
    this.loadInitialData();
  }

  setFromWidgetDelete(value: boolean): void {
    this.fromWidgetDelete = value;
    console.log(this.fromWidgetDelete);
  }

  getFromWidgetDelete(): boolean {
    return this.fromWidgetDelete;
  }

  // Loads initial data into the ReplaySubject
  private loadInitialData(): void {
    this.get_all_announcement_api().subscribe(
      (data) => this.announcements.next(data),
      (error) => this.announcements.error(error)
    );
  }

  get_all_announcement_api(): Observable<Announcement[]> {
    return this.http.get<Announcement[]>('/api/announcements');
  }

  get_all_auth_announcement(): Observable<Announcement[]> {
    return this.http.get<Announcement[]>('/api/announcements/all');
  }

  create_announcement_api(
    announcement: Announcement
  ): Observable<Announcement> {
    return this.http.post<Announcement>('/api/announcements', announcement);
  }

  update_announcement_api(
    announcement: Announcement
  ): Observable<Announcement> {
    return this.http.put<Announcement>('/api/announcements', announcement);
  }

  delete_announcement_slug(slug: string): Observable<void> {
    this.setFromWidgetDelete(true);
    return this.http.delete<void>('/api/announcements/' + slug).pipe(
      tap(() => {
        this.changes.emit();
      })
    );
  }

  get_announcement_by_slug(slug: string): Observable<Announcement> {
    return this.http.get<Announcement>('/api/announcements/' + slug);
  }
}
