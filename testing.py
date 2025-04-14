def _activate_powers_up(self,ans,trigger,se):
    if getattr(self.settings,trigger) and ans == trigger:
        active_attr = f"{trigger}_active"
        start_attr = f"{trigger}_start"
        setattr(self.settings,active_attr, True)
        self._play_powersup_se(se)
        setattr(self.settings,start_attr,pygame.time.get_ticks())
