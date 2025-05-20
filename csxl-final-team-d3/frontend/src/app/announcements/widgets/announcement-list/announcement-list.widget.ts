import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Announcement } from '../../announcement.model';
//import { Organization } from 'src/app/organization/organization.model';

@Component({
  selector: 'announcement-list',
  templateUrl: './announcement-list.widget.html',
  styleUrls: ['./announcement-list.widget.css']
})
export class AnnouncementList {
  /** The event for the event card to display */
  @Input() announcementsPerDay: [string, Announcement[]][] = [];

  /** The organization associated with the Event List for the Organization Details Page */
  //@Input() organization: Organization | null = null;

  /** Store the selected Event */
  @Input() selectedAnnouncement: Announcement | null = null;

  /** Whether or not to disable the links on the page */
  @Input() disableLinks: boolean = false;

  @Input() showHeader: boolean = false;

  /** Whether or not to disable the event creation button */
  @Input() showCreateButton: boolean = false;

  /** Whether or not the event list should be full width */
  @Input() fullWidth: boolean = false;

  /** Event binding for the card's on click action */
  @Output() cardClicked: EventEmitter<Announcement> = new EventEmitter();

  /** Constructs the widget */
  constructor() {}
}
