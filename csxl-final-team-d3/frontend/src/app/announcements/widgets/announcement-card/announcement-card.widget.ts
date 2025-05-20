import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Announcement } from '../../announcement.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AnnouncementService } from '../../announcement.service';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { Profile } from 'src/app/models.module';
import { Router } from '@angular/router';
import { AnnouncementsComponent } from '../../announcements-start/announcements.component';

@Component({
  selector: 'announcement-card',
  templateUrl: './announcement-card.widget.html',
  styleUrls: ['./announcement-card.widget.css']
})
export class AnnouncementCard {
  /** Inputs and outputs go here */
  @Input() announcement!: Announcement;
  //@Input() profile!: Profile;
  @Input() disableLink!: Boolean;
  @Input() selected: Boolean = false;
  @Output() clicked = new EventEmitter<Announcement>();
  @Output() deleteSuccess = new EventEmitter<void>();
  public adminPermission$: Observable<boolean>;
  public showAdminControls: boolean = true;
  defaultImage: string = 'assets/favicon.png';
  defaultImageLoaded: boolean = false;

  /** Constructor */
  constructor(
    private announcementService: AnnouncementService,
    private router: Router,
    private snackBar: MatSnackBar,
    private permission: PermissionService
  ) {
    this.adminPermission$ = this.permission.check(
      'announcements.edit',
      `announcement/${this.announcement?.slug}`
    );
  }

  toggleAdminControls(): void {
    this.showAdminControls = !this.showAdminControls;
  }

  updateState(announcement: Announcement): void {
    const updatedData = { ...announcement };
    updatedData.state = announcement.state;
    this.announcementService.update_announcement_api(updatedData).subscribe({
      next: () => {
        this.snackBar.open(
          'Announcement state updated successfully!',
          'Close',
          { duration: 3000 }
        );
      },
      error: (err) => {
        console.error('Failed to update the announcement state:', err);
        this.snackBar.open('Failed to update the state', 'Close', {
          duration: 3000
        });
      }
    });
  }

  /** Handler for when the event card is pressed */
  cardClicked() {
    if (this.disableLink) {
      this.clicked.emit(this.announcement);
    }
  }

  /** Runs when the edit button is pressed (navigate to the edit page) */
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
          this.deleteSuccess.emit();
        },
        error: (err) => {
          console.error('Failed to delete the announcement:', err);
          this.snackBar.open('Failed to delete the announcement', 'Close', {
            duration: 3000
          });
        }
      });
  }

  onImageError(event: Event): void {
    if (!this.defaultImageLoaded) {
      const element = event.target as HTMLImageElement;
      element.src = this.defaultImage;
      this.defaultImageLoaded = true;
    }
  }
}
