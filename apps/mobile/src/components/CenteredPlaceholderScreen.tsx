import { StyleSheet, Text, View } from 'react-native';

import { COLORS } from '@/src/theme/colors';
import { LAYOUT, SPACING } from '@/src/theme/layout';
import { TYPOGRAPHY } from '@/src/theme/typography';

type CenteredPlaceholderScreenProps = {
  title: string;
  subtitle: string;
};

export function CenteredPlaceholderScreen({
  title,
  subtitle,
}: CenteredPlaceholderScreenProps) {
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.subtitle}>{subtitle}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: LAYOUT.flexFull,
    alignItems: 'center',
    justifyContent: 'center',
    padding: SPACING.lg,
    backgroundColor: COLORS.backgroundPrimary,
  },
  title: {
    fontSize: TYPOGRAPHY.fontSizeTitle,
    fontWeight: TYPOGRAPHY.fontWeightBold,
    color: COLORS.textPrimary,
  },
  subtitle: {
    marginTop: SPACING.sm,
    fontSize: TYPOGRAPHY.fontSizeBody,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
});



