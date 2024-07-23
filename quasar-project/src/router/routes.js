const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/main', component: () => import('pages/MainPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  // client id : 65896343084-arc4inpsmt2fl459cl2b7iik3gagbm08.apps.googleusercontent.com
  // client secret : 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
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
