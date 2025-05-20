import { Component, inject } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { Profile, PublicProfile } from 'src/app/profile/profile.service';
import { Announcement, State } from '../announcement.model';
import { AnnouncementService } from '../announcement.service';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { PermissionService } from 'src/app/permission.service';
import { Organization } from 'src/app/organization/organization.model';
import { Observable, map } from 'rxjs';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { DatePipe } from '@angular/common';
import { animate } from '@angular/animations';

@Component({
  selector: 'app-create-announcements',
  templateUrl: './create-announcements.component.html',
  styleUrls: ['./create-announcements.component.css']
})
export class CreateAnnouncementsComponent {
  public static Route: Route = {
    path: 'edit/:slug',
    component: CreateAnnouncementsComponent,
    title: 'Edit Announcement',
    canActivate: [isAuthenticated],
    resolve: {
      profile: profileResolver
    }
  };

  public announcement: Announcement;

  public profile: Profile | null = null;
  /** Store the currently-logged-in user's profile.  */
  public authors: PublicProfile[] = [];

  /** Store the announcement id. */
  announcement_slug: string = 'default';
  announcement_id: number = 0;

  /** Add validators to the form */
  id = new FormControl(0, [Validators.required]);
  headline = new FormControl('', [Validators.required]);
  synopsis = new FormControl('', [Validators.required]);
  main_story = new FormControl('', [Validators.required]);
  organization = new FormControl('');
  state = new FormControl('', [Validators.required]);
  slug = new FormControl('', [
    Validators.required,
    Validators.pattern('^(?!new$)[a-z0-9-]+$')
  ]);
  image = new FormControl('');
  publish = new FormControl('', [Validators.required]);
  modification = new FormControl('', [Validators.required]);

  public announcementForm = this.formBuilder.group({
    id: this.id,
    headline: this.headline,
    synopsis: this.synopsis,
    main_story: this.main_story,
    organization: this.organization,
    state: State.Draft,
    slug: this.slug,
    image: this.image,
    publish: [
      this.dataPipe.transform(new Date(), 'yyyy-MM-ddTHH:mm:ss'),
      Validators.required
    ],
    modification: [
      this.dataPipe.transform(new Date(), 'yyyy-MM-ddTHH:mm:ss'),
      Validators.required
    ],
    author_id: this.profile?.id
  });

  isNew: boolean = false;

  constructor(
    private announcementService: AnnouncementService,
    private route: ActivatedRoute,
    private router: Router,
    protected formBuilder: FormBuilder,
    protected snackBar: MatSnackBar,
    private permission: PermissionService,
    private dataPipe: DatePipe
  ) {
    /** Initialize data from resolvers. Get current user */
    const data = this.route.snapshot.data as {
      profile: Profile;
      announcement: Announcement;
    };
    this.profile = data.profile;
    this.announcement = data.announcement || this.createDefaultAnnouncement();
    this.announcement.author_id = data.profile.id;
    this.isNew = route.snapshot.params['slug'] == 'default';

    let announcement_slug = this.route.snapshot.params['slug'];
    this.announcement_slug = announcement_slug;

    /** Set organization form data */

    if (!this.isNew) {
      this.slug = route.snapshot.params['slug'];
      announcementService
        .get_announcement_by_slug(announcement_slug)
        .subscribe((announcement) => {
          this.announcementForm.setValue({
            id: announcement.id,
            headline: announcement.headline,
            synopsis: announcement.synopsis,
            main_story: announcement.main_story,
            organization: announcement.organization,
            state: announcement.state,
            slug: announcement.slug,
            image: announcement.image,
            publish: announcement.publish,
            modification: this.dataPipe.transform(
              new Date(),
              'yyyy-MM-ddTHH:mm:ss'
            ),
            author_id: announcement.author_id
          });
        });
    } else {
      this.announcementForm.setValue({
        id: this.announcement.id,
        headline: this.announcement.headline,
        synopsis: this.announcement.synopsis,
        main_story: this.announcement.main_story,
        organization: this.announcement.organization,
        state: this.announcement.state,
        slug: this.announcement.slug,
        image: this.announcement.image,
        publish:
          this.announcement.publish ||
          this.dataPipe.transform(new Date(), 'yyyy-MM-ddTHH:mm:ss'),
        modification:
          this.announcement.modification ||
          this.dataPipe.transform(new Date(), 'yyyy-MM-ddTHH:mm:ss'),
        author_id: this.announcement.author_id
      });
    }

    /** Get id from the url */
    this.announcement_slug = this.route.snapshot.params['slug'];
  }

  /** Event handler to handle submitting the Update Organization Form.
   * @returns {void}
   */
  onSubmit(): void {
    if (this.announcementForm.valid) {
      Object.assign(this.announcement, this.announcementForm.value);
      if (this.announcement_slug === 'default') {
        this.announcementService
          .create_announcement_api(this.announcement)
          .subscribe({
            next: (announcement) => this.onSuccess(announcement),
            error: (err) => this.onError(err)
          });
      } else {
        console.log(this.announcement);
        this.announcementService
          .update_announcement_api(this.announcement)
          .subscribe({
            next: (announcement) => this.onSuccess(announcement),
            error: (err) => this.onError(err)
          });
      }
    } else {
      this.snackBar.open('Please fill all required fields.', '', {
        duration: 2000
      });
    }
  }

  /** Event handler to handle cancelling the editor and going back to
   * the previous organization page.
   * @returns {void}
   */
  onCancel(): void {
    this.router.navigate([`announcement/${this.announcement_slug}`]);
  }

  /** Event handler to handle the first change in the organization name field
   * Automatically generates a slug from the organization name (that can be edited)
   * @returns {void}
   */
  generateSlug(): void {
    const headline = this.announcementForm.controls['headline'].value;
    const slug = this.announcementForm.controls['slug'].value;
    if (headline && !slug) {
      var generatedSlug = headline.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-');
      this.announcementForm.setControl('slug', new FormControl(generatedSlug));
    }
  }

  /** Opens a confirmation snackbar when an organization is successfully updated.
   * @returns {void}
   */
  private onSuccess(announcement: Announcement): void {
    this.router.navigate(['/announcement']);

    let message: string =
      this.announcement_slug === 'default'
        ? 'Announcement Created'
        : 'Announcement Updated';

    this.snackBar.open(message, '', { duration: 2000 });
  }

  /** Opens a snackbar when there is an error updating an organization.
   * @returns {void}
   */
  private onError(err: any): void {
    let message: string =
      this.announcement_slug === 'default'
        ? 'Error: Announcement Not Created'
        : 'Error: Announcement Not Updated';

    this.snackBar.open(message, '', {
      duration: 2000
    });
  }

  private createDefaultAnnouncement(): Announcement {
    return {
      id: 0,
      headline: '',
      synopsis: '',
      main_story: '',
      organization: '',
      state: State.Draft,
      slug: '',
      image: '',
      publish: '',
      modification: '',
      author_id: 1
    };
  }
}
