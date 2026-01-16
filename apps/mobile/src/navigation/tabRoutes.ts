export const TAB_ROUTES = [
  { name: 'index', title: 'Accueil', iconName: 'flash' },
  { name: 'chat', title: 'Chat', iconName: 'chatbubbles' },
  { name: 'notes', title: 'Notes', iconName: 'document-text' },
  { name: 'profile', title: 'Profil', iconName: 'person' },
] as const;

export type TabRouteName = (typeof TAB_ROUTES)[number]['name'];



