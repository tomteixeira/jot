import Ionicons from '@expo/vector-icons/Ionicons';
import { Tabs } from 'expo-router';

import { TAB_ROUTES } from '@/src/navigation/tabRoutes';
import { COLORS } from '@/src/theme/colors';

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: COLORS.textPrimary,
        tabBarInactiveTintColor: COLORS.textSecondary,
      }}
    >
      {TAB_ROUTES.map((route) => {
        const iconName =
          route.iconName as React.ComponentProps<typeof Ionicons>['name'];

        return (
          <Tabs.Screen
            key={route.name}
            name={route.name}
            options={{
              title: route.title,
              tabBarIcon: ({ color, size }) => (
                <Ionicons name={iconName} size={size} color={color} />
              ),
            }}
          />
        );
      })}
    </Tabs>
  );
}


