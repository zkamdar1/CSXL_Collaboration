import {
  Component,
  HostListener,
  OnInit,
  ViewChild,
  ElementRef
} from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { map, switchMap, take } from 'rxjs/operators';
import { Announcement } from '../announcement.model';
import { AnnouncementService } from '../announcement.service';
import { PermissionService } from 'src/app/permission.service';

@Component({
  selector: 'app-announcements',
  templateUrl: './announcements.component.html',
  styleUrls: ['./announcements.component.css']
})
export class AnnouncementsComponent implements OnInit {
  public static Route = {
    path: '',
    component: AnnouncementsComponent
  };

  @ViewChild('carousel') carousel!: ElementRef<HTMLDivElement>;
  public currentDate: Date = new Date();
  public viewingDate: Date = new Date();
  public visibleAnnouncements: Announcement[] = [];
  public selectedAnnouncement: Announcement | null = null;
  public adminPermission$: Observable<boolean>;
  public innerWidth: any;
  public groupedAnnouncements$!: Observable<Map<string, Announcement[]>>;

  constructor(
    public announcementService: AnnouncementService,
    public router: Router,
    private permission: PermissionService
  ) {
    this.adminPermission$ = this.permission.check(
      'announcements.create',
      `announcement/${this.selectedAnnouncement?.slug}`
    );
  }

  ngOnInit(): void {
    this.innerWidth = window.innerWidth;
    this.loadData();

    this.announcementService.changes.subscribe(() => {
      this.loadData();
    });
  }

  loadData(): void {
    this.groupedAnnouncements$ = this.adminPermission$.pipe(
      switchMap((isAdmin) =>
        isAdmin
          ? this.announcementService.get_all_auth_announcement()
          : this.announcementService.get_all_announcement_api()
      ),
      map((announcements) => this.groupAnnouncementsByDate(announcements))
    );
    this.groupedAnnouncements$.subscribe({
      next: (grouped) => {
        this.updateVisibleAnnouncements(grouped);
      },
      error: (err) => console.error('Error loading announcements:', err)
    });
  }

  private groupAnnouncementsByDate(
    announcements: Announcement[]
  ): Map<string, Announcement[]> {
    const grouped = new Map<string, Announcement[]>();

    announcements.sort((a, b) => {
      return (
        new Date(b.modification).getTime() - new Date(a.modification).getTime()
      );
    });
    announcements.forEach((announcement) => {
      const dateKey = new Date(announcement.publish).toDateString();
      const existing = grouped.get(dateKey) || [];
      existing.push(announcement);
      grouped.set(dateKey, existing);
    });

    return grouped;
  }

  private updateVisibleAnnouncements(
    grouped: Map<string, Announcement[]>
  ): void {
    const dateKey = this.viewingDate.toDateString();
    if (grouped.has(dateKey)) {
      const allAnnouncements = grouped.get(dateKey) ?? [];
      this.visibleAnnouncements = allAnnouncements;
    } else {
      this.visibleAnnouncements = [];
      console.log('No announcements for:', dateKey);
    }
  }

  scrollLeft(): void {
    this.adjustDate(-1);
  }

  scrollRight(): void {
    this.adjustDate(1);
  }

  private adjustDate(offset: number): void {
    const newDate = new Date(this.viewingDate);
    newDate.setDate(this.viewingDate.getDate() + offset);
    this.viewingDate = newDate;
    this.loadAnnouncementsForDate(newDate);
  }

  private loadAnnouncementsForDate(date: Date): void {
    this.groupedAnnouncements$
      .pipe(
        take(1),
        map((grouped) => this.filterAnnouncementsByDate(grouped, date))
      )
      .subscribe({
        next: (filtered) => this.updateVisibleAnnouncements(filtered),
        error: (err) => console.error('Error adjusting date view:', err)
      });
  }

  private filterAnnouncementsByDate(
    grouped: Map<string, Announcement[]>,
    date: Date
  ): Map<string, Announcement[]> {
    const dateKey = date.toDateString();
    const filtered = new Map<string, Announcement[]>();
    const announcements = grouped.get(dateKey);
    if (announcements) {
      filtered.set(dateKey, announcements);
    }
    return filtered;
  }

  navigateToCreationForm() {
    // Navigate to the announcement creation form
    this.router.navigate(['announcement/edit/default']);
  }

  @HostListener('window:resize')
  onResize(_: UIEvent) {
    // Update the browser window width
    this.innerWidth = window.innerWidth;
  }

  onAnnouncementCardClicked(announcement: Announcement) {
    this.selectedAnnouncement = announcement;
    this.announcementService
      .get_announcement_by_slug(announcement.slug)
      .subscribe({
        next: (detailedAnnouncement) => {
          this.selectedAnnouncement = detailedAnnouncement;
        },
        error: (error) => {
          console.error('Failed to fetch detailed announcement', error);
        }
      });
  }
}
