import { Component, Input, OnInit } from '@angular/core';
import { Announcement } from '../../announcement.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AnnouncementService } from '../../announcement.service';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { PermissionService } from 'src/app/permission.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'announcement-detail-card',
  templateUrl: './announcement-detail-card.widget.html',
  styleUrls: ['./announcement-detail-card.widget.css']
})
export class AnnouncementDetailCard implements OnInit {
  @Input() announcement!: Announcement;
  public adminPermission$: Observable<boolean>;
  defaultImage: string = 'assets/favicon.png';
  defaultImageLoaded: boolean = false;

  constructor(
    protected snackBar: MatSnackBar,
    protected announcementService: AnnouncementService,
    private route: ActivatedRoute,
    private router: Router,
    private permission: PermissionService
  ) {
    this.adminPermission$ = this.permission.check(
      'announcements.edit',
      `announcement/${this.announcement?.slug}`
    );
  }

  ngOnInit(): void {
    if (!this.announcement) {
      // Load announcement if not provided via input
      const slug = this.route.snapshot.paramMap.get('slug');
      if (slug) {
        this.announcementService.get_announcement_by_slug(slug).subscribe({
          next: (announcement) => (this.announcement = announcement),
          error: (error) => {
            console.error('Failed to fetch announcement', error);
            this.snackBar.open(
              'Failed to load announcement details.',
              'Close',
              {
                duration: 3000
              }
            );
          }
        });
      }
    }
  }

  editAnnouncement() {
    this.router.navigate(['/announcement/edit', this.announcement.slug]);
  }

  deleteAnnouncement() {
    this.announcementService
      .delete_announcement_slug(this.announcement.slug)
      .subscribe({
        next: () => {
          this.snackBar.open('Announcement deleted successfully!', 'Close', {
            duration: 3000
          });
          this.announcementService.get_all_announcement_api();
        },
        error: (err) => {
          console.error('Failed to delete the announcement:', err);
          this.snackBar.open('Failed to delete the announcement', 'Close', {
            duration: 3000
          });
        }
      });
    this.router.navigate(['/announcement']);
  }

  onImageError(event: Event): void {
    if (!this.defaultImageLoaded) {
      const element = event.target as HTMLImageElement;
      element.src = this.defaultImage; // Use the class member defaultImage
      this.defaultImageLoaded = true;
    }
  }
}
